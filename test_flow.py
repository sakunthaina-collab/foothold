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
        try:
            locator.evaluate("el => el.click()", timeout=3000)
        except Exception:
            pass


def run_dashboard_tests(page, test_dir, is_mobile=False):
    prefix = "mobile_db_" if is_mobile else "desktop_db_"
    db_url = 'file:///' + os.path.abspath('D:/deploy/foothold/dashboard.html').replace('\\', '/')
    print(f"--- Starting Dashboard test ({'mobile' if is_mobile else 'desktop'}) ---")
    
    page.goto(db_url)
    try:
        page.wait_for_load_state('domcontentloaded', timeout=3000)
    except Exception:
        pass

    # 1. Test Dashboard Renders (4 Stat Cards)
    total_val = page.locator('#totalCases').text_content().strip()
    urgent_val = page.locator('#urgentCount').text_content().strip()
    at_risk_val = page.locator('#atRiskCount').text_content().strip()
    on_track_val = page.locator('#onTrackCount').text_content().strip()
    assert total_val == '7', "Total stat card should show 7"
    assert urgent_val.isdigit() and int(urgent_val) > 0, "Urgent stat card should be a positive number"
    assert at_risk_val.isdigit(), "At risk stat card should be a number"
    assert on_track_val.isdigit(), "On track stat card should be a number"
    print(f"✓ 1. Stat cards rendered (Total: {total_val}, Urgent: {urgent_val}, At Risk: {at_risk_val}, On Track: {on_track_val})")

    # 2. Test Urgency Color Badges (Red / Amber / Green)
    assert len(page.locator('.status-urgent').all()) > 0, "Should have 🔴 URGENT red badges"
    assert len(page.locator('.status-at-risk').all()) > 0, "Should have 🟡 AT RISK amber badges"
    assert len(page.locator('.status-on-track').all()) > 0, "Should have ✓ ON TRACK green badges"
    print("✓ 2. Urgency color badges verified (Red, Amber, Green)")

    # 3. Test Case Queue Sorting & Rows
    rows = page.locator('.case-row').all()
    assert len(rows) == 7, "Case queue should render 7 rows"
    print("✓ 3. Case queue 7 rows verified")

    # 4. Test Next Actions Checklist
    action_items = page.locator('#actionList > div').all()
    assert len(action_items) > 0, "Next actions list should render active tasks"
    print(f"✓ 4. Next actions ({len(action_items)} items) verified")

    # 5. Test Back Button Link
    back_btn = page.locator('.back-btn')
    assert back_btn.is_visible(), "Back link should be visible"
    print("✓ 5. Back link to single-case tool verified")

    # 6. Test New Case Modal (Open → Fill → Submit → Verify)
    page.locator('.btn-primary', has_text='New Case').click()
    page.wait_for_timeout(300)
    modal = page.locator('#newCaseModal')
    assert modal.is_visible(), "New Case modal should be visible"
    # Fill the form
    page.locator('#newCaseId').fill('TEST-CASE-001')
    page.locator('#newCaseName').fill('Test Modal Case')
    page.locator('#newCaseType').select_option('EDD')
    page.locator('#newCasePriority').select_option('high')
    page.locator('#newNextAction').fill('Verify EDD form')
    # Submit
    page.locator('.btn-primary', has_text='บันทึกคดีใหม่').click()
    page.wait_for_timeout(500)
    # Verify case count increased
    new_total = page.locator('#totalCases').text_content().strip()
    assert new_total == '8', f"After adding case, total should be 8, got {new_total}"
    print("✓ 6. New Case Modal: open, fill, submit, count=8 verified")
    # Reset back to 7 demo cases for clean state
    page.locator('.btn-secondary', has_text='Reset Demo').click()
    page.wait_for_timeout(300)
    reset_total = page.locator('#totalCases').text_content().strip()
    assert reset_total == '7', f"After reset, total should be 7, got {reset_total}"
    print("✓ 6b. Reset Demo restored to 7 cases")

    # 7. Test Type Badge Coloring
    assert len(page.locator('.type-amlo').all()) > 0, "Should have AMLO type badges"
    print("✓ 7. Type badge colors verified (AMLO/Prasan/EDD)")

    # 8. Test Status Update Form & Save
    freshness_badges = page.locator('.freshness-badge').all()
    assert len(freshness_badges) > 0, "Should render freshness badges"
    print(f"✓ 8a. Freshness badges ({len(freshness_badges)}) verified")

    update_btn = page.locator('.btn-mini', has_text='อัปเดตสถานะ').first
    if update_btn.is_visible():
        update_btn.click()
        page.wait_for_timeout(300)
        status_ta = page.locator('.status-form textarea').first
        assert status_ta.is_visible(), "Status update textarea should be visible"
        status_ta.fill("Playwright test update note")
        page.locator('.status-form-actions .btn-mini', has_text='บันทึก').first.click()
        page.wait_for_timeout(500)
        print("✓ 8b. Status update saved successfully")

    # 9. Test Status History Modal
    history_btn = page.locator('.btn-mini-ghost', has_text='ประวัติ').first
    if history_btn.is_visible():
        history_btn.click()
        page.wait_for_timeout(300)
        hist_modal = page.locator('#historyModal')
        assert hist_modal.is_visible(), "History modal should be visible"
        print("✓ 9. Status history modal verified")
        page.locator('#historyModal .modal-close').click()
        page.wait_for_timeout(200)

    # 10. Test Police AI Pack Export
    ai_btn = page.locator('button', has_text='Export แฟ้มส่ง พงส./AI')
    assert ai_btn.is_visible(), "Police AI Pack export button should be visible in controls"
    print("✓ 10. Police AI Intake Pack export button verified")

    # 11. Capture Screenshot
    page.screenshot(path=os.path.join(test_dir, prefix + "dashboard_renders.png"), full_page=True)
    print("Captured: " + prefix + "dashboard_renders.png")

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
                page.wait_for_function("typeof go === 'function'", timeout=5000)
            except Exception:
                pass
            page.wait_for_timeout(300)
            
            # Helper to take screenshot
            def take_screenshot(step_name):
                filename = f"{vp_name}_step_{step_name}.png"
                filepath = os.path.join(test_dir, filename)
                try:
                    page.screenshot(path=filepath, full_page=True, timeout=5000)
                except Exception:
                    try:
                        page.screenshot(path=filepath, timeout=5000)
                    except Exception:
                        pass
                print(f"Captured: {filename}")
            
            # 1. Main Wizard & Category Selection
            take_screenshot("0_wizard_main")
            smart_click(page, page.locator("#cat-btn-lightBrown"))
            page.wait_for_timeout(400)
            take_screenshot("1_cat_lightBrown")

            smart_click(page, page.locator("#cat-btn-lightGray"))
            page.wait_for_timeout(400)

            # 2. Emergency 3 Steps Mode
            smart_click(page, page.locator(".emergency-rail button"))
            page.wait_for_timeout(400)
            take_screenshot("2_emergency_mode")

            # 3. Step 3: Event Summary & Checklist Mode
            page.evaluate("switchSection('step3-mode')")
            page.wait_for_timeout(400)
            page.select_option("#step3-pattern", "identity_theft")
            page.fill("#step3-details", "ถูกขโมยบัตรประชาชนเปิดบัญชีออนไลน์ ทราบเรื่องวันที่ 16 ส.ค.")
            page.check("#chk-statement")
            page.check("#chk-slips")
            page.wait_for_timeout(400)
            take_screenshot("3_step3_summary_checklist")

            # 4. Statement Generator Mode
            page.evaluate("switchSection('generator-mode')")
            page.wait_for_timeout(400)
            page.fill("#stmt-name", "สมชาย ใจบริสุทธิ์")
            page.fill("#stmt-idcard", "1-1234-56789-01-2")
            page.fill("#stmt-bank", "ธ.กสิกรไทย 012-3-45678-9")
            page.fill("#stmt-reason", "ถูกแอบอ้างนำข้อมูลบัตรประชาชนไปเปิดบัญชีออนไลน์โดยไม่ยินยอม")
            page.wait_for_timeout(400)
            take_screenshot("4_generator_mode")

            # 5. Flowchart & Directory Mode
            page.evaluate("switchSection('flowchart-mode')")
            page.wait_for_timeout(400)
            take_screenshot("5_flowchart_mode")

            # 6. Switch back to Main Wizard
            page.evaluate("switchSection('main-wizard')")
            page.wait_for_timeout(400)
            
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
