#!/usr/bin/env python3
"""
Research visible X timeline trends and emit a strict JSON artifact.

Assumptions:
- X is reachable and the chosen browser profile is already authenticated.
- A language model is available. ChatBrowserUse is preferred when
  BROWSER_USE_API_KEY is configured.
"""

import argparse
import asyncio
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

load_dotenv()

from browser_use import Agent, BrowserProfile, BrowserSession, ChatBrowserUse, ChatGoogle, ChatOpenAI
from browser_use.browser.events import ClickElementEvent, ScrollEvent
from browser_use.browser.profile import ViewportSize
from browser_use.llm.base import BaseChatModel
from browser_use.skill_cli.utils import find_chrome_executable

TARGET_TIMELINE_URL = 'https://x.com/i/timeline'
DEFAULT_OUTPUT_PATH = Path('./output/news-radar.json')


class VisibleSignal(BaseModel):
	post_text: str | None = None
	author_handle: str | None = None
	timestamp_text: str | None = None
	source_links: list[str] = Field(default_factory=list)
	evidence_note: str
	topic_hint: str | None = None
	confirmation_links_checked: list[str] = Field(default_factory=list)


class NavigationOutcome(BaseModel):
	status: Literal[
		'timeline_confirmed',
		'blue_icon_not_visible',
		'notifications_missing',
		'page_not_usable',
		'navigation_failed',
	]
	actual_url: str | None = None
	clicked_notification_text: str | None = None
	notes: str


class TimelineExtractionOutcome(BaseModel):
	status: Literal['ok', 'gated', 'empty', 'error']
	actual_url: str
	notes: str
	visible_post_count: int = 0
	sources_checked: list[str] = Field(default_factory=list)
	signals: list[VisibleSignal] = Field(default_factory=list)


class ScrapedPost(BaseModel):
	post_id: str
	post_text: str | None = None
	author_handle: str | None = None
	timestamp_text: str | None = None
	age_minutes: int | None = None
	source_links: list[str] = Field(default_factory=list)
	evidence_note: str


class ScrapeArtifact(BaseModel):
	generated_at: str
	time_window_hours: float
	post_count: int
	sources_checked: list[str]
	notes: str
	posts: list[ScrapedPost]


class StructuredRunError(Exception):
	def __init__(self, code: str, message: str, actual_url: str | None = None, sources_checked: list[str] | None = None):
		super().__init__(message)
		self.code = code
		self.message = message
		self.actual_url = actual_url
		self.sources_checked = sources_checked or []


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description='Run X trend research and emit strict JSON.')
	parser.add_argument('--output', default=str(DEFAULT_OUTPUT_PATH), help='Where to save the JSON artifact')
	parser.add_argument('--user-data-dir', default=None, help='Chrome user data directory for an authenticated profile')
	parser.add_argument('--profile-directory', default='Default', help='Chrome profile directory name')
	parser.add_argument('--model', default=None, help='Optional model override')
	parser.add_argument('--time-window-hours', type=float, default=6.0, help='Scrape posts with visible timestamps within this window')
	parser.add_argument('--max-scrolls', type=int, default=20, help='Maximum downward scrolls while collecting posts')
	parser.add_argument('--headless', action='store_true', help='Run headless')
	parser.add_argument('--debug', action='store_true', help='Enable browser-use logging')
	return parser.parse_args()


def configure_logging(debug: bool) -> None:
	if debug:
		os.environ['BROWSER_USE_SETUP_LOGGING'] = 'true'
		os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'info'
	else:
		os.environ['BROWSER_USE_SETUP_LOGGING'] = 'false'
		os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'error'


def build_llm(model_name: str | None) -> BaseChatModel:
	if os.getenv('BROWSER_USE_API_KEY'):
		return ChatBrowserUse(model=model_name or 'bu-latest')
	if os.getenv('GOOGLE_API_KEY'):
		return ChatGoogle(model=model_name or 'gemini-flash-latest', api_key=os.getenv('GOOGLE_API_KEY'), temperature=0.0)
	if os.getenv('OPENAI_API_KEY'):
		return ChatOpenAI(model=model_name or 'gpt-4.1-mini', temperature=0.0)
	raise StructuredRunError(
		code='missing_llm_credentials',
		message='Set BROWSER_USE_API_KEY, GOOGLE_API_KEY, or OPENAI_API_KEY before running this script.',
	)


def build_browser_session(args: argparse.Namespace) -> BrowserSession:
	viewport = ViewportSize(width=1440, height=1200)
	user_data_dir = (
		args.user_data_dir
		or os.getenv('USER_DATA_DIR')
		or os.getenv('BROWSER_USE_USER_DATA_DIR')
		or os.getenv('CHROME_USER_DATA_DIR')
	)

	if user_data_dir:
		executable_path = find_chrome_executable()
		if executable_path is None:
			raise StructuredRunError(code='chrome_not_found', message='Chrome executable not found for local profile mode.')
		profile = BrowserProfile(
			executable_path=executable_path,
			user_data_dir=user_data_dir,
			profile_directory=args.profile_directory,
			headless=args.headless,
			keep_alive=True,
			minimum_wait_page_load_time=1.0,
			wait_for_network_idle_page_load_time=1.0,
			wait_between_actions=1.0,
			viewport=viewport,
		)
		return BrowserSession(browser_profile=profile)

	return BrowserSession.from_system_chrome(
		profile_directory=args.profile_directory,
		headless=args.headless,
		keep_alive=True,
		minimum_wait_page_load_time=1.0,
		wait_for_network_idle_page_load_time=1.0,
		wait_between_actions=1.0,
		viewport=viewport,
	)


async def wait_until_page_usable(browser_session: BrowserSession, timeout_seconds: int = 45) -> str:
	deadline = datetime.now(timezone.utc) + timedelta(seconds=timeout_seconds)
	last_url = ''
	while datetime.now(timezone.utc) < deadline:
		state = await browser_session.get_browser_state_summary(include_screenshot=False)
		last_url = state.url or ''
		title = state.title or ''
		selector_map = state.dom_state.selector_map if state.dom_state else {}
		if ('x.com' in last_url or 'twitter.com' in last_url) and (len(selector_map) >= 5 or 'X' in title):
			return last_url
		await asyncio.sleep(1.0)
	raise StructuredRunError(
		code='page_not_usable',
		message='X home page did not become usable within the timeout.',
		actual_url=last_url or None,
		sources_checked=['https://x.com/home'],
	)


async def run_navigation_step(browser_session: BrowserSession, llm: BaseChatModel) -> NavigationOutcome:
	await browser_session.navigate_to('https://x.com/home')
	await wait_until_page_usable(browser_session)
	notifications_index = await find_notifications_nav_index(browser_session)
	if notifications_index is None:
		return NavigationOutcome(status='notifications_missing', actual_url=await browser_session.get_current_page_url(), notes='Notifications navigation item was not found.')
	await click_index(browser_session, notifications_index)
	await asyncio.sleep(2.0)
	current_url = await browser_session.get_current_page_url()
	if 'notifications' not in current_url:
		await browser_session.navigate_to('https://x.com/notifications')
		await asyncio.sleep(2.0)

	candidates = await find_notification_candidates(browser_session)
	if not candidates:
		return NavigationOutcome(
			status='blue_icon_not_visible',
			actual_url=await browser_session.get_current_page_url(),
			notes='No visible "New post notifications for ..." items were found to use as blue-icon notification candidates.',
		)

	for index, text in candidates:
		await click_index(browser_session, index)
		await asyncio.sleep(3.0)
		actual_url = await browser_session.get_current_page_url()
		if actual_url == TARGET_TIMELINE_URL:
			return NavigationOutcome(
				status='timeline_confirmed',
				actual_url=actual_url,
				clicked_notification_text=text,
				notes='Browser session URL verification matched the target timeline URL.',
			)
		await browser_session.navigate_to('https://x.com/notifications')
		await asyncio.sleep(2.0)

	return NavigationOutcome(
		status='navigation_failed',
		actual_url=await browser_session.get_current_page_url(),
		notes='Tried visible "New post notifications for ..." candidates, but none navigated to the target timeline URL.',
	)


async def extract_timeline_signals(browser_session: BrowserSession, llm: BaseChatModel) -> TimelineExtractionOutcome:
	target_url_hint = 'https://x.com' + '/i/timeline'
	prompt = f"""
You are on the X timeline research page.

Goal:
- Inspect only the currently visible posts on screen after arriving at {target_url_hint}.
- Collect candidate trend signals from directly visible content.

For each visible signal include:
- post_text
- author_handle if visible
- timestamp_text if visible
- source_links if visible
- evidence_note describing what was directly observed
- topic_hint if obvious
- confirmation_links_checked only if you opened a linked source page for confirmation

Rules:
- Do not scroll unless needed to stabilize the current view.
- Do not invent missing details.
- If the page is partially gated, extract only what is directly visible and explain that in notes.
- If there are no usable visible posts, return status "empty" or "gated".
- Prefer direct source inspection when needed, but only for links directly visible from the current posts.
- Include {target_url_hint} in sources_checked. Add any opened source pages too.
"""

	agent = Agent(
		task=prompt,
		llm=llm,
		browser_session=browser_session,
		output_model_schema=TimelineExtractionOutcome,
		use_vision=False,
		directly_open_url=False,
		use_judge=False,
	)
	history = await agent.run(max_steps=25)
	result = history.structured_output
	if result is None:
		raise StructuredRunError(code='extraction_parse_failed', message='Failed to parse timeline extraction output.')
	return result


def parse_timestamp_to_minutes(timestamp_text: str | None) -> int | None:
	if not timestamp_text:
		return None
	text = timestamp_text.strip().lower()
	match = re.fullmatch(r'(\d+)(s|m|h|d)', text)
	if match:
		value = int(match.group(1))
		unit = match.group(2)
		multiplier = {'s': 0, 'm': 1, 'h': 60, 'd': 60 * 24}[unit]
		return value * multiplier
	return None


def build_post_id(signal: VisibleSignal) -> str:
	base = '|'.join(
		[
			(signal.author_handle or '').strip(),
			(signal.timestamp_text or '').strip(),
			(signal.post_text or '').strip(),
		]
	)
	base = re.sub(r'\s+', ' ', base).strip()
	return re.sub(r'[^a-zA-Z0-9]+', '-', base.lower()).strip('-')[:80] or 'post'


def dedupe_sources(urls: list[str]) -> list[str]:
	deduped_sources: list[str] = []
	for url in urls:
		if url and url not in deduped_sources:
			deduped_sources.append(url)
	return deduped_sources


async def click_index(browser_session: BrowserSession, index: int) -> None:
	element = await browser_session.get_dom_element_by_index(index)
	if element is None:
		raise StructuredRunError(code='missing_click_target', message=f'Clickable element {index} was not found.')
	event = browser_session.event_bus.dispatch(ClickElementEvent(node=element))
	await event
	await event.event_result(raise_if_none=False, raise_if_any=True)


async def find_notifications_nav_index(browser_session: BrowserSession) -> int | None:
	state = await browser_session.get_browser_state_summary(include_screenshot=False)
	for index, element in state.dom_state.selector_map.items():
		text = element.get_all_children_text(max_depth=2).strip().lower()
		aria_label = str(element.attributes.get('aria-label', '')).strip().lower()
		if text == 'notifications' or aria_label.startswith('notifications'):
			return index
	return None


async def find_notification_candidates(browser_session: BrowserSession) -> list[tuple[int, str]]:
	state = await browser_session.get_browser_state_summary(include_screenshot=False)
	candidates: list[tuple[int, str]] = []
	for index, element in state.dom_state.selector_map.items():
		text = element.get_all_children_text(max_depth=4).strip()
		if 'New post notifications for' not in text:
			continue
		candidates.append((index, re.sub(r'\s+', ' ', text)))

	def sort_key(item: tuple[int, str]) -> tuple[int, int, str]:
		text = item[1].lower()
		return (
			0 if 'elon musk' in text else 1,
			1 if ' and ' in text else 0,
			text,
		)

	candidates.sort(key=sort_key)
	return candidates


async def scroll_down(browser_session: BrowserSession, amount: int = 900) -> int:
	before = await browser_session.get_browser_state_summary(include_screenshot=False)
	before_scroll_y = before.page_info.scroll_y if before.page_info else 0
	event = browser_session.event_bus.dispatch(ScrollEvent(direction='down', amount=amount))
	await event
	await event.event_result(raise_if_none=False, raise_if_any=True)
	await asyncio.sleep(1.0)
	after = await browser_session.get_browser_state_summary(include_screenshot=False)
	return (after.page_info.scroll_y if after.page_info else 0) - before_scroll_y


async def collect_recent_posts(
	browser_session: BrowserSession,
	llm: BaseChatModel,
	time_window_hours: float,
	max_scrolls: int,
) -> tuple[list[ScrapedPost], list[str], str]:
	limit_minutes = int(time_window_hours * 60)
	collected: list[ScrapedPost] = []
	seen_ids: set[str] = set()
	sources_checked: list[str] = [TARGET_TIMELINE_URL]
	notes: list[str] = []
	consecutive_out_of_window = 0
	skipped_without_timestamp = 0

	for scroll_index in range(max_scrolls + 1):
		extraction = await extract_timeline_signals(browser_session, llm)
		if extraction.actual_url != TARGET_TIMELINE_URL:
			raise StructuredRunError(
				code='timeline_url_mismatch',
				message=f'Expected extraction on {TARGET_TIMELINE_URL} but got {extraction.actual_url}',
				actual_url=extraction.actual_url,
				sources_checked=extraction.sources_checked or [TARGET_TIMELINE_URL],
			)
		if extraction.status in {'gated', 'error'}:
			raise StructuredRunError(
				code=f'timeline_{extraction.status}',
				message=extraction.notes,
				actual_url=extraction.actual_url,
				sources_checked=extraction.sources_checked or [TARGET_TIMELINE_URL],
			)

		sources_checked = dedupe_sources(sources_checked + extraction.sources_checked)
		new_recent_found = 0
		visible_in_window = 0
		visible_out_of_window = 0

		for signal in extraction.signals:
			age_minutes = parse_timestamp_to_minutes(signal.timestamp_text)
			if age_minutes is None:
				skipped_without_timestamp += 1
				continue
			if age_minutes > limit_minutes:
				visible_out_of_window += 1
				continue
			visible_in_window += 1
			post_id = build_post_id(signal)
			if post_id in seen_ids:
				continue
			seen_ids.add(post_id)
			collected.append(
				ScrapedPost(
					post_id=post_id,
					post_text=signal.post_text,
					author_handle=signal.author_handle,
					timestamp_text=signal.timestamp_text,
					age_minutes=age_minutes,
					source_links=dedupe_sources(signal.source_links + signal.confirmation_links_checked),
					evidence_note=signal.evidence_note,
				)
			)
			new_recent_found += 1

		if visible_in_window == 0 and visible_out_of_window > 0:
			consecutive_out_of_window += 1
		elif new_recent_found > 0:
			consecutive_out_of_window = 0

		if scroll_index == max_scrolls:
			notes.append(f'Reached max scroll limit ({max_scrolls}).')
			break

		if consecutive_out_of_window >= 2:
			notes.append('Stopped after consecutive views showed only posts older than the requested time window.')
			break

		scroll_delta = await scroll_down(browser_session)
		if scroll_delta <= 0:
			notes.append('Stopped because downward scrolling no longer changed the page position.')
			break

	if skipped_without_timestamp:
		notes.append(f'Skipped {skipped_without_timestamp} visible posts because no parseable relative timestamp was visible.')
	if not notes:
		notes.append('Collected posts by repeatedly extracting visible timeline items and scrolling downward.')
	collected.sort(key=lambda post: (post.age_minutes if post.age_minutes is not None else 10**9, post.post_id))
	return collected, sources_checked, ' '.join(notes)


def build_artifact(
	posts: list[ScrapedPost],
	sources_checked: list[str],
	time_window_hours: float,
	notes: str,
) -> ScrapeArtifact:
	return ScrapeArtifact(
		generated_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
		time_window_hours=time_window_hours,
		post_count=len(posts),
		sources_checked=dedupe_sources(sources_checked) or [TARGET_TIMELINE_URL],
		notes=notes,
		posts=posts,
	)


def build_error_artifact(error: StructuredRunError, time_window_hours: float) -> ScrapeArtifact:
	sources_checked = error.sources_checked or ([error.actual_url] if error.actual_url else [TARGET_TIMELINE_URL])
	notes = f'ERROR[{error.code}]: {error.message}'
	if error.actual_url:
		notes += f' Actual URL: {error.actual_url}'
	return ScrapeArtifact(
		generated_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
		time_window_hours=time_window_hours,
		post_count=0,
		sources_checked=[url for url in sources_checked if url],
		notes=notes,
		posts=[],
	)


def write_artifact(artifact: ScrapeArtifact, output_path: Path) -> None:
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(artifact.model_dump_json(indent=2), encoding='utf-8')


async def run_research(args: argparse.Namespace) -> ScrapeArtifact:
	llm = build_llm(args.model)
	browser_session = build_browser_session(args)
	await browser_session.start()

	try:
		try:
			navigation = await run_navigation_step(browser_session, llm)
		except Exception as error:
			raise StructuredRunError(code='navigation_step_failed', message=str(error), sources_checked=['https://x.com/home']) from error
		final_url = (await browser_session.get_browser_state_summary(include_screenshot=False)).url
		if navigation.status == 'blue_icon_not_visible':
			raise StructuredRunError(
				code='blue_icon_not_visible',
				message='No visible notification item with a blue icon was found.',
				actual_url=final_url or navigation.actual_url,
				sources_checked=['https://x.com/home'],
			)
		if navigation.status != 'timeline_confirmed':
			raise StructuredRunError(
				code=navigation.status,
				message=navigation.notes,
				actual_url=final_url or navigation.actual_url,
				sources_checked=['https://x.com/home'],
			)
		if final_url != TARGET_TIMELINE_URL:
			raise StructuredRunError(
				code='timeline_url_mismatch',
				message=f'Expected final URL {TARGET_TIMELINE_URL} but got {final_url}',
				actual_url=final_url,
				sources_checked=['https://x.com/home'],
			)

		try:
			posts, sources_checked, notes = await collect_recent_posts(
				browser_session=browser_session,
				llm=llm,
				time_window_hours=args.time_window_hours,
				max_scrolls=args.max_scrolls,
			)
		except Exception as error:
			raise StructuredRunError(
				code='timeline_collection_failed',
				message=str(error),
				actual_url=final_url or TARGET_TIMELINE_URL,
				sources_checked=[TARGET_TIMELINE_URL],
			) from error
		if not posts:
			raise StructuredRunError(
				code='no_recent_posts',
				message='No visible posts with parseable timestamps were within the requested time window.',
				actual_url=TARGET_TIMELINE_URL,
				sources_checked=sources_checked or [TARGET_TIMELINE_URL],
			)
		return build_artifact(posts, sources_checked, args.time_window_hours, notes)
	finally:
		await browser_session.stop()


async def async_main() -> int:
	args = parse_args()
	configure_logging(args.debug)
	output_path = Path(args.output)

	try:
		artifact = await run_research(args)
		write_artifact(artifact, output_path)
		print(artifact.model_dump_json(indent=2))
		return 0
	except StructuredRunError as error:
		artifact = build_error_artifact(error, args.time_window_hours)
		write_artifact(artifact, output_path)
		print(artifact.model_dump_json(indent=2))
		return 1
	except Exception as error:
		artifact = build_error_artifact(StructuredRunError(code='unexpected_error', message=str(error)), args.time_window_hours)
		write_artifact(artifact, output_path)
		print(artifact.model_dump_json(indent=2))
		return 1


def main() -> None:
	raise SystemExit(asyncio.run(async_main()))


if __name__ == '__main__':
	main()
