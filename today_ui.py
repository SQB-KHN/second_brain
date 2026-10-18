"""Timeline-first local planner UI; all task content rendered as plain text."""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import streamlit as st
import config
from retro_studio_ui import topbar
from task_service import Tasks, for_day, local_time


def render(navigate, dark=False):
    st.markdown('''<style>
    .stApp h1{font-family:Georgia,serif}.st-key-today-mobile{display:none}.today-rail{border-left:3px solid #c297ac;padding:1rem;background:#f1e5eb;border-radius:0 18px 18px 0;margin:.6rem 0;font-family:Georgia,serif}
    @media(max-width:640px){.st-key-today-mobile{display:block;position:fixed;bottom:0;left:0;right:0;background:var(--background-color);z-index:999;padding:.5rem 1rem;border-top:1px solid #c297ac}.block-container{padding-bottom:7rem!important}.st-key-today-desktop{display:none}.st-key-today-mobile [data-testid="stHorizontalBlock"]{flex-wrap:nowrap}.st-key-today-mobile [data-testid="stColumn"]{width:0!important;min-width:0!important;flex:1 1 0!important}.today-rail{padding:.7rem} }
    </style>''', unsafe_allow_html=True)
    if not dark:
        st.markdown('<style>.stApp{background:#faf5f2!important}</style>', unsafe_allow_html=True)
    st.caption('YOUR DAY, WITH INTENTION · LOCAL PLANNER')
    st.title('Make today yours.')
    st.caption('Your rhythm · Your priorities · Your little digital universe')
    topbar('my_day.exe')
    with st.container(key='today-desktop'):
        nav = st.columns(2)
        nav[0].button('Research', on_click=navigate, args=('Ask',), use_container_width=True)
        nav[1].button('Analytics', on_click=navigate, args=('Analyse',), use_container_width=True)
    with st.container(key='today-mobile'):
        mobile = st.columns(3)
        for col, label, target in zip(mobile, ('Today', 'Research', 'Analytics'), ('Today', 'Ask', 'Analyse')):
            col.button(label, key='mobile_'+label, on_click=navigate, args=(target,), use_container_width=True)
    with st.expander('◷ Calendar controls · day, view and timezone', expanded=False):
        controls = st.columns([2, 1, 2])
    day = controls[0].date_input('Planning day', value=date.today())
    mode = controls[1].selectbox('Planning view', ('Day', 'Week'))
    zone = controls[2].text_input('Display timezone', value='UTC')
    try:
        ZoneInfo(zone)
    except Exception:
        st.error('Enter an IANA timezone, such as Asia/Kolkata.')
        return
    if config.DEPLOY_MODE:
        st.info('Synthetic examples · read only. Private planner storage is never opened.')
        records = [dict(id='sample', title='Plan a focused morning', details='Synthetic example', status='todo', priority=1,
                        scheduled_start=local_time(f'{day}T09:00', zone), scheduled_end=local_time(f'{day}T10:00', zone), due=None, project='Sample')]
        store = None
    else:
        try:
            store = Tasks()
            records = store.list()
        except Exception:
            st.error('Planner unavailable. No changes saved. Check local permissions or restore a verified backup; see docs/today.md.')
            return
    schedule, due, unscheduled = for_day(records, day, zone)
    seen = {}
    def card(r, timed=False):
        seen[r['id']] = seen.get(r['id'], 0) + 1
        key = r['id'] + str(seen[r['id']])
        import html
        palette = {
            1: ('#7e9dd3', '#deebfb'),
            2: ('#8bb780', '#e0f1d9'),
            3: ('#d99a82', '#fce9db'),
        }
        accent, shade = palette[r['priority']]
        time_label = 'Unscheduled'
        if timed:
            a, b = (datetime.fromisoformat(r[k]).astimezone(ZoneInfo(zone)) for k in ('scheduled_start', 'scheduled_end'))
            time_label = f'{a:%H:%M} – {b:%H:%M}'
        status_label = 'Done' if r['status'] == 'done' else r['status'].capitalize()
        title = html.escape(r['title'])
        meta = html.escape(' · '.join(filter(None, [r.get('project'), status_label, f'P{r["priority"]}'])))
        st.markdown(
            '<div class="retro-timeline"><div class="retro-time">'
            + html.escape(time_label)
            + '</div><div class="retro-task" style="--task-accent:' + accent
            + ';--task-bg:' + shade + '"><div class="retro-task-title">'
            + title + '</div><div class="retro-task-meta">' + meta
            + '</div></div></div>',
            unsafe_allow_html=True,
        )
        if r['details']:
            st.caption(r['details'])
        if store:
            cols = st.columns(2)
            if cols[0].button('Edit / reschedule', key='edit'+key):
                st.session_state.planner_edit = r['id']
                st.session_state.planner_edit_version = r['updated']
                st.rerun()
            if cols[1].button('Complete', key='complete'+key, disabled=r['status'] == 'done'):
                try:
                    save_existing(store, r, status='done')
                    st.rerun()
                except Exception:
                    st.error('Could not save. Reload and try again.')
    timeline, focus = st.columns([2.15, 1], gap='large')
    with focus:
        st.subheader('★ Three priorities')
        candidates = [r for r in records if r['status'] != 'done' and (r in schedule or r in due or r in unscheduled)]
        for i, r in enumerate(candidates[:3], 1):
            st.text(f"{i:02} · P{r['priority']} · {r['title']}")
        if not candidates:
            st.caption('Room to focus. Add a task when you are ready.')
    with timeline:
        if mode == 'Day':
            st.subheader('◷ Daily rhythm')
            for r in schedule:
                card(r, True)
            if not schedule:
                st.caption('No scheduled time. Due dates and unscheduled tasks stay separate.')
        else:
            st.subheader('▦ Weekly rhythm')
            monday = day - timedelta(days=day.weekday())
            for offset in range(7):
                d = monday + timedelta(days=offset)
                st.write(d.strftime('%A · %d %B'))
                scheduled, due_day, _ = for_day(records, d, zone)
                for r in scheduled:
                    card(r, True)
                for r in due_day:
                    st.text('Due · '+r['title'])
    st.subheader('Due on selected day')
    for r in due:
        card(r)
    st.subheader('Unscheduled')
    for r in unscheduled:
        card(r)
    overdue = [r for r in records if r.get('due') and r['due'] < day.isoformat() and r['status'] != 'done']
    if overdue:
        st.subheader('Overdue')
        for r in overdue:
            st.text('Due '+r['due'])
            card(r)
    if store:
        with st.expander('✎ Create or edit a task', expanded=bool(st.session_state.get('planner_edit'))):
            editor(store, records, zone)


def save_existing(store, record, **changes):
    fields = {k: record[k] for k in ('title', 'details', 'status', 'priority', 'scheduled_start', 'scheduled_end', 'due', 'project', 'references')}
    fields.update(timezone_id=record['timezone'], task_id=record['id'], expected_updated=record['updated'])
    fields.update(changes)
    return store.save(**fields)


def editor(store, records, zone):
    selected = st.session_state.get('planner_edit')
    r = next((r for r in records if r['id'] == selected), {})
    st.subheader('Edit task' if r else 'New task')
    if r and st.button('Cancel edit / new task'):
        st.session_state.pop('planner_edit', None)
        st.rerun()
    with st.form('task_form_'+str(selected)):
        title = st.text_input('Task title', value=r.get('title', ''))
        details = st.text_area('Details', value=r.get('details', ''))
        status = st.selectbox('Task status', ('todo', 'doing', 'done'), index=('todo', 'doing', 'done').index(r.get('status', 'todo')))
        priority = st.selectbox('Priority', (1, 2, 3), index=r.get('priority', 2)-1)
        project = st.text_input('Project label', value=r.get('project', ''))
        tz = st.text_input('Task timezone', value=r.get('timezone', zone))
        scheduled = st.checkbox('Schedule this task', value=bool(r.get('scheduled_start')))
        st.caption('Leave times empty for unscheduled tasks. Dates use YYYY-MM-DD; local times use YYYY-MM-DDTHH:MM.')
        def wall(key):
            return datetime.fromisoformat(r[key]).astimezone(ZoneInfo(r['timezone'])).strftime('%Y-%m-%dT%H:%M') if r.get(key) else ''
        start = st.text_input('Scheduled start', value=wall('scheduled_start'))
        end = st.text_input('Scheduled end', value=wall('scheduled_end'))
        choices = ('Require explicit choice', 'First occurrence', 'Second occurrence')
        start_occurrence = st.selectbox('Repeated hour at start', choices)
        end_occurrence = st.selectbox('Repeated hour at end', choices)
        due = st.text_input('Due date (optional)', value=r.get('due') or '')
        refs = st.text_area('Related local files (one relative path per line)', value='\n'.join(r.get('references', [])))
        if st.form_submit_button('Save task'):
            try:
                folds = {'Require explicit choice': None, 'First occurrence': 0, 'Second occurrence': 1}
                store.save(task_id=r.get('id'), expected_updated=st.session_state.get('planner_edit_version'), title=title, details=details, status=status,
                           priority=priority, project=project, timezone_id=tz, due=due or None,
                           scheduled_start=local_time(start, tz, folds[start_occurrence]) if scheduled else None,
                           scheduled_end=local_time(end, tz, folds[end_occurrence]) if scheduled else None, references=[s.strip() for s in refs.splitlines() if s.strip()])
                st.session_state.pop('planner_edit', None)
                st.rerun()
            except (ValueError, KeyError):
                st.error('Invalid task. Check title, dates, timezone, repeated-hour choice, local references, and whether another session changed this task.')
            except Exception:
                st.error('Save failed. Nothing committed; reload and retry or check local storage.')
    try:
        project_rows = store.projects()
    except Exception:
        st.error('Projects unavailable. Check local storage and reload.')
        return
    projects = {r['id']: r['label'] for r in project_rows}
    if projects:
        with st.expander('Project status'):
            pid = st.selectbox('Project', list(projects), format_func=projects.get)
            current = next(r['status'] for r in project_rows if r['id'] == pid)
            status = st.selectbox('Project status', ('active', 'done'), index=('active', 'done').index(current))
            if st.button('Save project status'):
                try:
                    store.project_status(pid, status)
                    st.success('Project status saved.')
                except Exception:
                    st.error('Project status could not be saved.')
