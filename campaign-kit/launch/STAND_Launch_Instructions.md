# STAND website and Track Her Case: launch instructions

You have three files:

| File | What it is |
|---|---|
| **STAND_website_upload.zip** | The complete website, ready to upload to xneelo |
| **Track_Her_Case_Campaign_Kit.zip** | Films, images, YouTube and BackaBuddy pictures, and the campaign guides |
| **This document** | Step-by-step instructions |

Allow about 30 minutes for Part 1. You need your xneelo login.

# Part 1: Put the website live

## Step 1. Back up the current website (5 minutes)

1. Log in to the xneelo control panel (xneelo.co.za, then **Log in**).
2. Open your hosting for **standaction.co.za** and click **File Manager**.
3. Open the folder **public_html**. This is where your current website lives.
4. Select everything inside public_html, click **Compress** (or **Download**), and save the file somewhere safe on your computer. If anything goes wrong, you can put this back.

Your email is not stored in public_html. Nothing in these steps touches info@ or board@.

## Step 2. Remove the old website files

1. Still inside public_html, select all the old files and folders.
2. Click **Delete**.

Only do this once the backup from Step 1 is saved on your computer.

## Step 3. Upload the new website

1. Inside the empty public_html folder, click **Upload**.
2. Choose **STAND_website_upload.zip** from your computer and wait until it shows 100%.
3. Click once on the zip in public_html to select it, then click **Extract** (it may say **Unzip**). Extract it into public_html.
4. Check that these now sit **directly inside public_html**, not inside another folder:
   - index.html, campaign.html, support.html and the other pages
   - the folders **assets**, **css**, **js**, **give** and **share**
   - the files **.htaccess**, **progress.txt** and **giving-links.txt**
5. Delete the zip from public_html.

Tip: .htaccess starts with a dot, so some file managers hide it. If you can't see it, look for **Settings** or **Show hidden files** in File Manager.

## Step 4. Switch on the security certificate (https)

1. In the xneelo control panel, find **SSL** for standaction.co.za. It is usually under the domain's web hosting settings.
2. Choose the free **Let's Encrypt** certificate for both **standaction.co.za** and **www.standaction.co.za**, and click **Enable** (or **Install**).
3. It can take up to an hour to become active. The website is set to switch to the secure address automatically once it is.

## Step 5. Check everything works (10 minutes)

Do these on your phone and your laptop:

- [ ] **standaction.co.za** shows the new homepage with the new logo
- [ ] **standaction.co.za/give** opens the campaign page
- [ ] On the homepage, **Live pilot** opens at "The Red Dot Process"
- [ ] On a phone, scroll down any page and tap the round menu button: the full menu opens
- [ ] **standaction.co.za/share** opens the WhatsApp share kit
- [ ] The campaign film plays on the campaign page
- [ ] Paste **standaction.co.za/give** into a WhatsApp chat with yourself: the preview shows the ambassador and the headline. (WhatsApp can take a few minutes, or up to a day, to pick up a brand-new page.)

If standaction.co.za still shows the old website after an hour, the domain may be pointing somewhere other than your xneelo hosting. Call xneelo support and ask them to confirm that standaction.co.za points to your xneelo web hosting.

# Part 2: Switch on GlobalGiving and BackaBuddy

Until you do this, those two buttons say "link coming soon". SnapScan and EFT work from day one. You can do this yourself, with no help from Claude:

1. In File Manager, open **public_html** and click **giving-links.txt**, then **Edit**.
2. You will see two lines:
   ```
   GlobalGiving:
   BackaBuddy:
   ```
3. Paste each campaign link after its name, with one space after the colon. For example:
   ```
   GlobalGiving: https://www.globalgiving.org/projects/your-project-name/
   BackaBuddy: https://www.backabuddy.co.za/campaign/your-campaign-name
   ```
4. Click **Save**. The buttons on the campaign page and the Support page switch on straight away. Refresh the page to check.

Copy each link from the address bar of your live campaign page, so it starts with **https://**. You can add one link now and the other later.

# Part 3: Update the progress bar

The campaign page shows how much has been raised towards R150,000.

1. In File Manager, open **public_html**, click **progress.txt**, then **Edit**.
2. Replace the number with the total raised so far **in rand**. Use digits only: no R, no spaces, no commas. For example, for R41,500 type `41500`.
3. Click **Save**. The bar updates for everyone straight away.

Add up SnapScan, EFT, BackaBuddy and GlobalGiving (converted to rand). Update it every few days, and always after a big day such as GivingTuesday. While it says 0, the page shows "Be one of the first to give" instead of a bar.

# Part 4: Launch the campaign

## Before you go public (now to 24 November)

- [ ] Website live (Part 1) and the giving links added (Part 2)
- [ ] GlobalGiving and BackaBuddy pages published, using **GlobalGiving_and_BackaBuddy_Page_Copy.docx** and the five pictures in the **backabuddy** folder of the campaign kit
- [ ] YouTube videos uploaded with titles, descriptions, thumbnails, end screens and pinned comments (**YouTube_Titles_Descriptions.docx**)
- [ ] Consent confirmed for everyone pictured, and for telling both women's stories anonymously
- [ ] Ten gifts from your inner circle before any public post. Use **standaction.co.za/share**: tap "Send on WhatsApp" on your personal message, one person at a time
- [ ] Share **standaction.co.za/share** with the Board and your champions, so they can send messages to their own circles
- [ ] One person asked to match gifts during the 16 Days (if someone says yes, send Claude their name and amount)
- [ ] Someone checking info@standaction.co.za daily for Section 18A requests

## Key dates

| Date | What to post | Which film |
|---|---|---|
| By 24 November | Personal WhatsApp asks to your 60 names | Attach the 24-second teaser |
| **25 November** | 16 Days launch post on every channel | Main film (vertical for Reels, TikTok and Shorts; square for LinkedIn and Facebook) |
| Every second day | WhatsApp Status, following days 1, 3, 5 and 7 in the share kit | As shown in the share kit |
| **1 December** | GivingTuesday: the biggest push | Main film, plus the match message if a match is in place |
| 10 December | Closing push and thank-you post | Teaser |
| Mid-December | Festive update to all donors with the total raised | |

Full captions for each platform are in **Social_Media_Posting_Guide.docx**. Your campaign pack (**Track_Her_Case_Fund_the_16_Days_Campaign_Pack.docx**) has the thank-you messages and the weekly rhythm.

## Every day of the campaign

- Thank every donor personally within 24 hours (the thank-you message is in the share kit)
- Reply to comments on social media within the first hour where you can
- Check the totals every Friday and update progress.txt

# Where everything is

| What | Where |
|---|---|
| Campaign page | standaction.co.za/give |
| WhatsApp share kit (for you and champions) | standaction.co.za/share |
| Project brief (PDF) | On the Track Her Case page, and in the campaign kit |
| Giving links | giving-links.txt on xneelo |
| Progress total | progress.txt on xneelo |
| Films, images and guides | Track_Her_Case_Campaign_Kit.zip |

If anything doesn't look right after uploading, send Claude a screenshot.
