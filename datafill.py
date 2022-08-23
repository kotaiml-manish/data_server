import time

from playwright.sync_api import sync_playwright

from threading import *

# This is change

class datafillup(Thread):
    ## variables for guest details
    def __init__(self):
        super().__init__()

    def run(self):
        print("thread 2 is getting started!!! and will wait")
        time.sleep(20)
        name = "Md Abid Hussain"
        ph_no = "9674367196"
        address = "17 B.G Road, SBI complex, Block B , Flat 5/2, kasba, kolkata"
        age = "30"
        arrived_from = "kolkata"
        house_no = "Block B, Flat 5/2"
        lane = "17 B.G Road"
        landmark = "SBI Complex"
        pin = "700042"
        id = "DL"
        id_number = "ZYR3065497"
        date = "12"
        enter_time = "00:10"
        room_no = "205"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            page = browser.new_page()
            page.goto('https://bbsrudp-atithi.com/login_index.php')
            page.fill('input#username', 'ADMIN001')
            page.fill('input#password', 'Bhinnasakala@2099')
            # Fill [placeholder="--Select Organisation--"]
            page.locator("[placeholder=\"--Select Organisation--\"]").fill("bh")

            # Click text=Bhinna Sakala >> nth=1
            page.locator("text=bhinna sakala").nth(0).click()

            page.locator("text=Sign in").click()
            # Click a:has-text("Activity")
            page.wait_for_load_state()
            page.locator("a:has-text(\"Activity\")").click()
            # Click a:has-text("Guest") >> nth=2
            page.locator("a:has-text(\"Guest\")").nth(2).click()
            # expect(page).to_have_url("https://bbsrudp-atithi.com/guest/visitor_list.php?role_code=T2dEdU1mU2s3MGJaL3dTVkhudlFQQT09")
            # Click button:has-text("Add Guest")
            page.locator("button:has-text(\"Add Guest\")").click()
            # Fill [placeholder="Enter Guest Name "]
            page.locator("[placeholder=\"Enter Guest Name \"]").fill(name)

            # Fill [placeholder="Enter Guest Mobile Number "]
            page.locator("[placeholder=\"Enter Guest Mobile Number \"]").fill(ph_no)

            # Fill [placeholder="Enter Age "]
            page.locator("[placeholder=\"Enter Age \"]").fill(age)
            # Select M
            page.locator("select[name=\"cmbGender\"]").select_option("M")

            # Fill [placeholder="Enter Guest From"]
            page.locator("[placeholder=\"Enter Guest From\"]").fill(arrived_from)
            # Select IND
            page.locator("select[name=\"cmbnationality\"]").select_option("IND")
            # Click text=* Means of Transport: Required >> input[type="text"]
            page.locator("text=* Means of Transport: Required >> input[type=\"text\"]").click()
            # Click text=Car
            page.locator("text=Car").click()
            # Click text=*Present Address : Required Required Required Required Select State Required Sel >> [placeholder="Plot\/House Number\/At"]
            page.locator(
                "text=*Present Address : Required Required Required Required Select State Required Sel >> [placeholder=\"Plot\\/House Number\\/At\"]").fill(
                house_no)
            # Click text=*Present Address : Required Required Required Required Select State Required Sel >> [placeholder="Lane"]

            page.locator(
                "text=*Present Address : Required Required Required Required Select State Required Sel >> [placeholder=\"Lane\"]").fill(
                lane)
            # Click text=*Present Address : Required Required Required Required Select State Required Sel >> [placeholder="Landmark"]

            page.locator(
                "text=*Present Address : Required Required Required Required Select State Required Sel >> [placeholder=\"Landmark\"]").fill(
                landmark)
            # page.wait_for_load_state()
            # Click .selectize-input.items.not-full >> nth=0
            page.locator(".selectize-input.items.not-full").first.click()
            # Click text=India >> nth=1
            page.locator("text=India").nth(1).click()
            # Click .selectize-input.items.not-full >> nth=0
            page.locator(".selectize-input.items.not-full").first.click()
            # Click text=Odisha
            page.locator("text=West Bengal").is_visible()
            page.locator("text=West Bengal").click()
            # Click .selectize-input.items.not-full >> nth=0
            page.locator(".selectize-input.items.not-full").first.click()
            # Click text=Sambalpur
            page.locator("text=Kolkata").click()
            page.locator(
                "text=*Present Address : Required Required Required IndiaIndiaOtherPakistanUSA Require >> [placeholder=\"Enter Town\"]").fill(
                "Kolkata")
            # Fill text=*Present Address : Required Required Required IndiaIndiaOtherPakistanUSA Require >> [placeholder="Enter PIN"]
            page.locator(
                "text=*Present Address : Required Required Required IndiaIndiaOtherPakistanUSA Require >> [placeholder=\"Enter PIN\"]").fill(
                pin)
            # Click text=Same As Present Required Required Required Required Select State Required Select >> ins
            page.locator(
                "text=Same As Present Required Required Required Required Select State Required Select >> ins").click()
            # Click .selectize-input.items.not-full >> nth=0
            page.locator(".selectize-input.items.not-full").first.click()
            # Click text=Aadhar
            page.locator("text=" + id).click()

            # Fill [placeholder="Enter Id Number"]
            page.locator("[placeholder=\"Enter Id Number\"]").fill(id_number)

            # Click [placeholder="Select Date"]
            page.locator("[placeholder=\"Select Date\"]").click()
            # Click text=13
            # page.locator("text=12").click()
            page.locator("td:has-text(\"12\")").nth(1).click()
            # Click [placeholder="Select Time"]
            page.locator("[placeholder=\"Select Time\"]").click()
            # Fill [placeholder="Select Time"]
            page.locator("[placeholder=\"Select Time\"]").fill(enter_time)

            # Fill [placeholder="Enter total Room booked Number\."]
            page.locator("[placeholder=\"Enter total Room booked Number\\.\"]").fill("1")
            # Click button[name="btnRoomDtls"]
            page.locator("button[name=\"btnRoomDtls\"]").click()
            # Click [placeholder="Enter Building Number"]
            # page.locator("[placeholder=\"Enter Building Number\"]").click()
            # Fill [placeholder="Enter Building Number"]
            page.locator("[placeholder=\"Enter Building Number\"]").fill(room_no)
            # Click [placeholder="Enter Floor Number"]
            # page.locator("[placeholder=\"Enter Floor Number\"]").click()
            # Fill [placeholder="Enter Floor Number"]
            page.locator("[placeholder=\"Enter Floor Number\"]").fill(room_no)
            # Click [placeholder="Enter Room Number"]
            # page.locator("[placeholder=\"Enter Room Number\"]").click()
            # Fill [placeholder="Enter Room Number"]
            page.locator("[placeholder=\"Enter Room Number\"]").fill(room_no)
            # Click ins >> nth=2
            page.locator("ins").nth(2).click()

            page.locator('text=Submit').click()
