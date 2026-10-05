import asyncio, json, glob
from playwright.async_api import async_playwright

async def audit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 390, "height": 844}) # Mobile viewport
        
        products = glob.glob("/root/projects/iviz-viral-products/dist/*.html")
        report = []
        
        for f in sorted(products):
            url = f"file://{f}"
            await page.goto(url)
            
            title = await page.title()
            body_text = await page.inner_text("body")
            
            # Check buttons & affiliate tags
            buttons = await page.query_selector_all("a[href*='invl.me']")
            btn_count = len(buttons)
            
            # Check for dummy/rekaan/placeholder words
            has_lorem = "lorem" in body_text.lower()
            has_tanpapromo = "tanpapromo" in body_text.lower()
            has_arbitrage = "arbitrage" in body_text.lower()
            
            # Check for CRO components
            has_pros = "Kelebihan" in body_text or "Kelebihan" in await page.content()
            has_cons = "Kekurangan" in body_text or "Kekurangan" in await page.content()
            has_verdict = "Keputusan Pantas" in body_text or "Keputusan Pantas" in await page.content()
            
            report.append({
                "file": f.split("/")[-1],
                "title": title[:50],
                "affiliate_buttons": btn_count,
                "clean_text": not (has_lorem or has_tanpapromo or has_arbitrage),
                "has_cro_elements": (has_pros and has_cons and has_verdict) if f.split("/")[-1] != "index.html" else True
            })
            
        await browser.close()
        print(json.dumps(report, indent=2))

asyncio.run(audit())
