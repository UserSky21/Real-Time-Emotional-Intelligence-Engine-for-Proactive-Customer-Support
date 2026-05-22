from bs4 import BeautifulSoup
import csv
import re
# --- NEW: Import the impersonating requests library ---
from curl_cffi import requests 
# ------------------------------------------------------

def format_review_url(url):
    match = re.search(r'/([A-Z0-9]{10})(?:[/?]|$)', url)
    if match:
        asin = match.group(1)
        print(f"Extracted ASIN: {asin}")
        return f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    return url 

def get_amazon_reviews_bs4(url):
    scrape_url = format_review_url(url)
    print(f"Targeting URL: {scrape_url}")

    # Keep your headers, but we don't need the massive Cookie anymore!
    # curl_cffi is stealthy enough to usually bypass the login wall entirely.
    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        # --- YOUR AUTHENTICATION BADGE ---
        "Cookie": 'session-id=136-8318348-0311126; lc-main=en_US; sp-cdn="L5Z9:IN"; skin=noskin; ubid-main=132-5731711-8924237; sso-state-main=Xdsso|ZQGxD_2jFMB25yr9imUQSiFtkC-FxtBo5woQYwR7MNwTyRbnj6c3_wK8SgXUyxaENz-mFJuoz9Yrzy9KLYN32kdrL8GX4CgRFXew9T6m3owGD4Nb; i18n-prefs=USD; at-main=Atza|gQA39DPhAwEBAkyusElxraacux-IuiGoMgEFW_38W4WKnJfu3yE4Y0GrknnO_Vcc41XP3kAkrY6BJv6Lfg673FffGTn8rsTaCig8NIG2XVEnxQKfqQik00RRVbJZm4Wi3xVdfdAMt2KqrdyjZ4XvYSJp1RMS9Bl9_1i_IJyvwPTQjJ6aahZQqkzcmYTtFZmuO-7GCkejzMPLXg2U2VJLDhgTTT5LSHdnb3Wj6lR99ZKodwWiJ2scInHrM_i9R3hg4ePS2oqnaYwBI2pn4EmcM0wHeN4kQOxr_EgVF--0PfBAmA7_c2EJ88YH01rxoCxIbm_9Rd6Asjb4sWR3DWcQK5EMFUdGssf2dZ3VS10D2Q69-Y1Cj7nrYitp4-paTI6U2g; sess-at-main=xDu2mppvNKBol3Qfqny8ZbWa6i4wd/H32Nap1evisFE=; sst-main=Sst1|PQJJSQvyujUzTaPhdap28LvPDe8JD6v5Jt294eoYQfmVYoWQ1DAeGxjb4ovlNsdctsXLkYtoV5DjViSBV3hRxgSXXntQPtNvkix5_x9S0ipiEW5Bie5sJoMKKylviZUp2OXdsPbo-QnvxmbLKxXWX3DzbTvNvF39t2KahYAKdI2OBuri7MpJqkLoEclq9rSONw01Z4-5CLQvTEWCld090hql5zWqwiRnPQEILJ0AxGzWADM9sGYiMaMjKgi3D5V8bVgJUpD0z5VJwQVTQI9jPqxWY4wIogiymnzcZL4EOkKf_ZCTpUivbHbHdE6yHDRWZVdNRPrjlrbFRVEm-Lc1cv_sDn6OrGIE1XYgHMVc1Y0zy6hkFm399OrK1fjWKTDU7SFC; session-id-time=2082787201l; ak_bmsc=C9CE35E225240AD5995F26C8CE2E8F08~000000000000000000000000000000~YAAQtgVaaMJ90T6eAQAARF6TTh9bwUx15jsrd9WQpXfvGFT2eNt1tTZKHch+l5nPSWjCREI7LSlCI+jduclYpshiNvB2nMmc/xJOem869EnvijMLkeZ9Fcy5puls7x3+66Y/4F3ocO76gRRv5hWQjwpedbxryHmpRS6ouKUa8REMR/C2eGoCzD1sh8sSSUtxU+3UWWubOPQxeTHvGBocIXE2c1FpSf2t8EJzL2DbY5aBgeVfAtooMajww7uHJqB0Ccq9Th1fu66l5nBoaI+xQ2jh3Rw4UhZvBOyhhphdI+MbacgvMwpOSeYoE7feCK371z9TvrHdYsWo6jvWhvTbZoolXpoVmn3wYx2GFqN60foP3cN5Nvt/RyZHp4cjT0suE8OjyP+7l52PNRSAzjbuGC/DmzlfstgQvwVaPQ==; bm_sv=10A8394D4D0C601BC37B4E74E992ECA6~YAAQtgVaaIOC0T6eAQAAv6CTTh/OkSjtCZ/M2sxFMaO272UjzjAc0a63hJOz1K1cE7+fLsENebxNT+l4QhXxKhcSVOJ1F7HlhkJES/qPMUi0tz6YH26FTFrxtDy2qC9H3NYJApXcgy47379a0N86ucW8vbUILHuPOX6QaZbaVwQyjvIqfJi1NpdCR6bpLW6LocgwKncIEMwgBG2vb9EqNcdNfpniL5MpNZmU4zAHQ1Mlgqr5BAsxE2ve88jgHMvo~1; session-token=pBGXf+geZ/Lq25xvK3P3J/LcBXhZ2+GWvSX1PRUEIhigaTZgpXw4RIJ0VFJOqs/cst8VH527k1f1JVi3HPC2VRhyyJxDuTOTSSW7IoFX6KaVpg41XcOhzvy42I5QXfeS4ht8WpVl6NVuK9SY75uZRHDIwjqN6L7Tw9wqsEuZyw8/jAqdRLVJocX2ga+FabtdQUMaPRYBptlTlGOWrEjj8tR8L2SlAa/HiF+HX185Gbu5r0jHuJ2fZdp9bRcaBE2k; x-main="UcctdNQp5Evp?OSbahaSoO6dBnrqtlOUpFPv1NgO9reR1iSCGXudL2s4bMqbgYaV"'
    }

    try:
        print("Sending request with Chrome TLS fingerprinting...")
        
        # --- NEW: The Impersonation Magic ---
        # impersonate="chrome120" tells the library to perfectly mimic a real Chrome browser's network signature
        response = requests.get(
            scrape_url, 
            headers=headers, 
            impersonate="chrome120", 
            timeout=15
        )
        # ------------------------------------
        
        if response.status_code == 503:
            print("FAILED: Hard WAF Block (503 Service Unavailable).")
            return
            
        response.raise_for_status()

        if "Type the characters you see in this image" in response.text or "captcha" in response.text.lower():
            print("FAILED: Hit a WAF Soft Block! Amazon returned a CAPTCHA.")
            with open('debug_captcha.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            return

        # Save for debugging
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        reviews = soup.find_all('span', {'data-hook': 'review-body'})
        
        if not reviews:
            reviews = soup.find_all('span', class_='review-text-content')

        comm = []
        for review in reviews:
            text = review.get_text(strip=True)
            if text:
                comm.append([text])

        if not comm:
            print("No reviews found. Open debug_page.html to see what the scraper actually downloaded.")
        else:
            print(f"Successfully scraped {len(comm)} reviews.")
            
            with open('./comment.csv', 'w', encoding="utf-8", newline='') as filee:
                writer = csv.writer(filee)
                writer.writerow(["Comments"])
                writer.writerows(comm)
            print("Saved to comment.csv")

    except Exception as e:
        print(f"Request failed: {e}")