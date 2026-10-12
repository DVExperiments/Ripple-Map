"""Browser integration tests (developer only; Playwright not required by app)."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SCREENS=ROOT/'tests/screenshots';SCREENS.mkdir(exist_ok=True,parents=True)
def mount(page,storage=None):
    page.goto('about:blank')
    page.set_content((ROOT/'index.html').read_text(encoding='utf-8'))
    page.evaluate("""(seed)=>{let data=new Map(Object.entries(seed||{}));Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>data.get(k)||null,setItem:(k,v)=>data.set(k,String(v)),removeItem:k=>data.delete(k),dump:()=>Object.fromEntries(data)}})}""",storage or {})
    page.add_style_tag(path=str(ROOT/'assets/styles.css'))
    for name in ['content.js','engine.js','app.js']:page.add_script_tag(path=str(ROOT/'assets'/name))
errors=[]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'])
    desktop=b.new_page(viewport={'width':1500,'height':950},accept_downloads=True,device_scale_factor=1)
    desktop.on('pageerror',lambda x:errors.append(str(x)))
    mount(desktop)
    assert desktop.locator('.scenario-card').count()==7
    desktop.screenshot(path=str(SCREENS/'home_desktop.png'),full_page=True)
    desktop.locator('[data-action="start"][data-id="ai-assistant"]').last.click()
    assert desktop.locator('#system-svg [data-node]').count()>=6
    assert desktop.locator('.lens.on').count()==2
    desktop.screenshot(path=str(SCREENS/'map_initial.png'),full_page=True)
    desktop.locator('[data-action="all-lenses"]').click()
    assert desktop.locator('.lens.on').count()==6
    assert desktop.locator('#system-svg [data-node]').count()==19
    for investigated in [x['id'] for x in json.loads((ROOT/'assets/content.json').read_text())['scenarios'][0]['nodes'][1:12]]:
        desktop.locator('#inspect-select').select_option(investigated)
    desktop.locator('#inspect-select').select_option('power')
    assert desktop.get_by_text('Reliable electricity',exact=False).count()>=1
    desktop.locator('[data-action="critical"]').click()
    desktop.locator('[data-field="justification"]').fill('Power is a critical dependency because a data centre needs electricity to operate reliably, although redundancy may help.')
    desktop.locator('[data-action="loop"]').click()
    assert desktop.get_by_role('dialog').count()==1
    desktop.locator('[data-action="close"]').last.click()
    assert desktop.get_by_role('dialog').count()==0
    desktop.screenshot(path=str(SCREENS/'map_revealed.png'),full_page=True)
    desktop.locator('[data-action="add-element"]').click()
    dialog=desktop.locator('#new-element')
    dialog.locator('[name="label"]').fill('Language accessibility')
    dialog.locator('[name="category"]').select_option('people')
    dialog.locator('[name="description"]').fill('Users may require interface translations and cultural context to interpret model responses.')
    dialog.locator('[name="other"]').select_option('core')
    dialog.locator('[name="kind"]').select_option('influences')
    dialog.locator('button[type="submit"]').click()
    assert desktop.locator('#system-svg [data-node]').count()==20
    assert desktop.get_by_text('YOUR HYPOTHESIS').count()>=1
    desktop.locator('[data-action="add-link"]').click()
    dialog=desktop.locator('#new-link')
    dialog.locator('[name="source"]').select_option('power')
    dialog.locator('[name="target"]').select_option('network')
    dialog.locator('[name="why"]').fill('Network facilities need power too, but redundancy should be investigated.')
    dialog.locator('button').last.click()
    # move node with pointer: test that edit persists without crashing
    svg=desktop.locator('#system-svg')
    g=desktop.locator('[data-node="power"]')
    bb=g.bounding_box();desktop.mouse.move(bb['x']+bb['width']/2,bb['y']+bb['height']/2);desktop.mouse.down();desktop.mouse.move(bb['x']+bb['width']/2+24,bb['y']+bb['height']/2+18,steps=6);desktop.mouse.up()
    desktop.locator('.stagebutton[data-stage="stress"]').click()
    desktop.locator('[data-action="incident"][data-id="power"]').click()
    assert desktop.locator('.impact-box').count()==1
    desktop.screenshot(path=str(SCREENS/'stress_desktop.png'),full_page=True)
    desktop.locator('[data-field="intervention"]').fill('Install appropriate backup power and test recovery procedures, but consider cost, maintenance and carbon effects.')
    desktop.locator('.stagebutton[data-stage="reflect"]').click()
    for name in ['boundary','people','unexpected','next']:
        desktop.locator('[data-reflect="'+name+'"]').fill('We should test these relationships against lived experiences, operator evidence and local conditions.')
    desktop.screenshot(path=str(SCREENS/'reflection_desktop.png'),full_page=True)
    desktop.locator('[data-action="finish"]').click()
    assert desktop.locator('.review-score').inner_text().startswith('100')
    desktop.screenshot(path=str(SCREENS/'review_desktop.png'),full_page=True)
    with desktop.expect_download() as d:desktop.locator('[data-action="export"]').first.click()
    assert 'Power' in Path(d.value.path()).read_text(encoding='utf-8')
    with desktop.expect_download() as d:desktop.locator('[data-action="export-svg"]').click()
    assert d.value.suggested_filename.endswith('.svg')
    with desktop.expect_download() as d:desktop.locator('[data-action="export-png"]').click()
    assert d.value.suggested_filename.endswith('.png')
    assert Path(d.value.path()).read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
    saved=desktop.evaluate('localStorage.dump()')
    mount(desktop,saved)
    desktop.locator('[data-action="history"]').click()
    assert desktop.locator('.history-card').count()==1
    with desktop.expect_download() as d:desktop.locator('[data-action="backup"]').click()
    backup=Path(d.value.path());content=json.loads(backup.read_text(encoding='utf-8'));assert content['app']=='ripple-map' and len(content['history'])==1
    desktop.locator('[data-action="open-history"]').click()
    assert desktop.locator('.review-score').inner_text().startswith('100')
    # Mobile
    mob=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1)
    mob.on('pageerror',lambda x:errors.append(str(x)))
    mount(mob)
    mob.screenshot(path=str(SCREENS/'home_mobile.png'),full_page=True)
    assert mob.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
    mob.locator('.scenario-card').first.click()
    mob.screenshot(path=str(SCREENS/'map_mobile.png'),full_page=True)
    assert mob.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
    assert mob.locator('#inspect-select').is_visible()
    b.close()
assert not errors,errors
print('PASS: catalog, map, layer discovery, inspector, critical choice, feedback loop, custom element/link, dragging, stress cascade, reflection, score, exports SVG PNG Markdown, saved history, mobile layout, no page errors')
