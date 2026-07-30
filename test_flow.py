# -*- coding: utf-8 -*-
import os
import sys
from playwright.sync_api import sync_playwright


def smart_click(page, locator):
    try:
        locator.scroll_into_view_if_needed(timeout=2000)
    except Exception:
        pass
    try:
        locator.click(timeout=3000)
    except Exception:
        locator.evaluate("el => el.click()")


def run_dashboard_tests(page, test_dir, is_mobile=False):
    prefix = "mobile_db_" if is_mobile else "desktop_db_"
    db_url = 'file:///' + os.path.abspath('D:/deploy/foothold/dashboard.html').replace('\\', '/')
    print(f"--- Starting Dashboard test ({'mobile' if is_mobile else 'desktop'}) ---")
    
    page.goto(db_url)
    try:
        page.wait_for_load_state('networkidle', timeout=3000)
    except Exception:
        pass

    # 1. Test Dashboard Renders
    assert page.locator('#totalCases').text_content().strip() == '7', "Total stat card should show 7"
    print("Captured: " + prefix + "dashboard_renders.png")
    page.screenshot(path=os.path.join(test_dir, prefix + "dashboard_renders.png"), full_page=True)

    # 2. Test Urgency Colors & Badges
    urgent_badges = page.locator('.status-urgent').all()
    assert len(urgent_badges) > 0, "Should have URGENT red badges"
    print("✓ Urgency badges verified")

    # 3. Test Case Rows
    rows = page.locator('.case-row').all()
    assert len(rows) > 0, "Case rows should be rendered"
    print(f"✓ {len(rows)} Case rows verified")

    print(f"Finished Dashboard test for {'mobile' if is_mobile else 'desktop'}")

def run_test():
    file_url = "file:///" + os.path.abspath("index.html").replace("\\", "/")
    
    test_dir = os.path.abspath("test")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        print(f"Created directory: {test_dir}")
        
    viewports = {
        "desktop": {"width": 1200, "height": 900},
        "mobile": {"width": 390, "height": 844}
    }
    
    # Store console messages
    console_errors = []
    
    with sync_playwright() as p:
        for vp_name, vp_size in viewports.items():
            print(f"\n--- Starting test for {vp_name} ({vp_size['width']}x{vp_size['height']}) ---")
            
            is_mobile = vp_name == "mobile"
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport=vp_size,
                is_mobile=is_mobile,
                has_touch=is_mobile
            )
            page = context.new_page()
            
            # Listen to console messages and errors
            def log_console(msg):
                if msg.type == "error":
                    err_msg = f"[{vp_name}] Console Error: {msg.text} at {msg.location}"
                    console_errors.append(err_msg)
                    print(err_msg)
                else:
                    print(f"[{vp_name}] Console {msg.type}: {msg.text}")
                    
            page.on("console", log_console)
            page.on("pageerror", lambda err: console_errors.append(f"[{vp_name}] Uncaught Exception: {err.message}"))
            
            # Load page
            page.goto(file_url)
            try:
                page.wait_for_load_state('networkidle', timeout=2000)
            except Exception:
                pass
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(600) # Allow CSS animations to finish
            
            # Helper to take screenshot
            def take_screenshot(step_name):
                filename = f"{vp_name}_step_{step_name}.png"
                filepath = os.path.join(test_dir, filename)
                page.screenshot(path=filepath, full_page=True)
                print(f"Captured: {filename}")
            
            # 1. Entry Page
            take_screenshot("0_entry")
            
            # Click start button (เริ่มทีละขั้น)
            page.get_by_text("เริ่มทีละขั้น").first.click(force=True)
            page.wait_for_timeout(600)
            
            # 2. Triage Page
            take_screenshot("1_triage")
            
            # Select "ม้าเทาอ่อน" (status grey_light)
            smart_click(page, page.get_by_text("เลือกสีม้าโดยตรง"))
            page.wait_for_timeout(600)
            smart_click(page, page.get_by_text("ม้าเทาอ่อน", exact=True))
            page.wait_for_timeout(600)
            
            # 3. Orient Page
            take_screenshot("2_orient")
            
            # Click next button (ระบุสถานการณ์ย่อย)
            smart_click(page, page.get_by_text("ระบุสถานการณ์ย่อย"))
            page.wait_for_timeout(600)
            
            # 3.5. Subcase Page
            take_screenshot("2_subcase")
            
            # Click first subcase option
            page.locator(".opt").first.click(force=True)
            page.wait_for_timeout(600)
            
            # 4. Pattern Select Page
            take_screenshot("3_pattern_select")
            
            # Select "ถูกหลอกผ่านประกาศรับสมัครงาน" (job pattern)
            smart_click(page, page.get_by_text("ถูกหลอกผ่านประกาศรับสมัครงาน", exact=True))
            page.wait_for_timeout(600)
            
            # 5. Pattern Detail Page
            take_screenshot("3_pattern_detail")
            
            # Click next button (เก็บข้อเท็จจริงของคุณ)
            smart_click(page, page.get_by_text("เก็บข้อเท็จจริงของคุณ"))
            page.wait_for_timeout(600)
            
            # 6. Facts Page
            take_screenshot("4_facts_empty")
            
            # Fill facts
            page.fill("#fn", "สมชาย ใจดี")
            page.fill("#fid", "1234567890123")
            page.fill("#fad", "123 ถ.สุขุมวิท กรุงเทพฯ")
            page.fill("#fph", "081-234-5678")
            page.fill("#fbk", "กรุงเทพ")
            page.fill("#fac", "123-4-56789-0")
            page.fill("#fci", "12345/2569")
            page.fill("#fbr", "REF987654")
            page.fill("#fof", "ร.ต.อ. รักธรรม")
            page.fill("#fst", "สน.ทุ่งมหาเมฆ")
            page.fill("#ffw", "20 มิ.ย. 2569")
            page.fill("#ffh", "โอนเงินผ่านแอปไม่ได้")
            page.fill("#fiv", "ถูกหลอกผ่านงานโพสต์รายได้สูง ให้สแกนหน้าและลงทะเบียน")
            page.wait_for_timeout(300)
            
            take_screenshot("4_facts_filled")
            
            # Click next (สร้างไทม์ไลน์)
            smart_click(page, page.get_by_text("สร้างไทม์ไลน์"))
            page.wait_for_timeout(600)
            
            # 7. Timeline Page
            take_screenshot("5_timeline")
            
            # Click next (เอกสารที่ต้องเตรียม)
            smart_click(page, page.get_by_text("เอกสารที่ต้องเตรียม"))
            page.wait_for_timeout(600)
            
            # 8. Docs Page
            # Tick all checkboxes
            checkboxes = page.locator("input[type='checkbox']")
            count = checkboxes.count()
            print(f"Found {count} checkboxes on Docs page")
            for i in range(count):
                checkboxes.nth(i).check(force=True)
            page.wait_for_timeout(300)
            take_screenshot("6_docs")
            
            # Click next (ถัดไป)
            smart_click(page, page.get_by_text("ถัดไป"))
            page.wait_for_timeout(600)
            
            # 8.5. Prep Page
            take_screenshot("7_prep")
            
            # Click next (ไปร่างคำร้องต่อ)
            smart_click(page, page.get_by_text("ไปร่างคำร้องต่อ"))
            page.wait_for_timeout(600)
            
            # 9. Petition Page
            take_screenshot("8_petition")
            
            # Click next (ขั้นสุดท้าย: ส่งต่อ)
            smart_click(page, page.get_by_text("ขั้นสุดท้าย: ส่งต่อ"))
            page.wait_for_timeout(600)
            
            # 9.5. Download Page
            take_screenshot("9_download")
            
            # Click next (ไปขั้นตอนส่งต่อ)
            smart_click(page, page.get_by_text("ไปขั้นตอนส่งต่อ"))
            page.wait_for_timeout(600)
            
            # 10. Next Page
            take_screenshot("10_next")
            
            run_dashboard_tests(page, test_dir, is_mobile=(vp_name == "mobile"))
            
            browser.close()
            print(f"Finished test for {vp_name}")

    print("\n" + "="*30)
    print("--- Test Run Summary ---")
    print(f"Total console errors/exceptions found: {len(console_errors)}")
    for err in console_errors:
        print(f" - {err}")
    print("="*30)
    
if __name__ == "__main__":
    run_test()
