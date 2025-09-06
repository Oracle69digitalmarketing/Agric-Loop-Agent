from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Listen for all console events and print them
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))

        try:
            # 1. Go to the application
            page.goto("http://127.0.0.1:8000/")

            # 2. Fill out and submit the form
            page.locator("#farmer_id").fill("+15559876543")
            page.locator("#text").fill("My crops have yellow spots")
            page.get_by_role("button", name="Submit Issue").click()

            # 3. Wait for the diagnosis button and click it
            diagnose_button = page.get_by_role("button", name="Diagnose")
            expect(diagnose_button).to_be_visible(timeout=5000)
            diagnose_button.click()

            # 4. Wait for the results and verify them
            results_div = page.locator("#results")
            expect(results_div).to_contain_text("Diagnosis:", timeout=5000)

            # 5. Take a screenshot
            page.screenshot(path="jules-scratch/verification/verification.png")
            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="jules-scratch/verification/error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
