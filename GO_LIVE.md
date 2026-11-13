# Putting the STAND website live on xneelo

You need two things: the file **STAND_website_upload.zip** and your xneelo login. The steps take about 15 minutes.

## 1. Save a copy of the current site (2 minutes)

1. Log in to the xneelo control panel and open **File Manager** for standaction.co.za. (If your plan has no File Manager, use FTP as in step 5.)
2. Open the **public_html** folder. Your current website lives there.
3. Select everything in public_html, then choose **Compress** (or **Download**) and save the archive somewhere safe. If anything goes wrong, you can put this back.

Your email is not stored in public_html, so nothing you do here touches info@ or board@.

## 2. Clear the old website files

In public_html, delete the old website files. If you see folders such as `wp-admin`, `wp-content` or `wp-includes`, the old site was WordPress. Delete those too, along with its loose files (index.php, wp-config.php and so on). Only do this after the backup in step 1.

## 3. Upload and unzip the new site

1. Still in public_html, click **Upload** and choose **STAND_website_upload.zip**.
2. When it has uploaded, select the zip and choose **Extract** (or **Unzip**) into public_html.
3. Check that **index.html**, **.htaccess**, **progress.txt** and the folders **assets**, **css**, **js** and **give** now sit directly inside public_html, not inside another folder.
4. Delete the zip from public_html.

Tip: `.htaccess` starts with a dot, so some file managers hide it. Look for a "show hidden files" option.

## 4. Turn on the free security certificate (https)

In the xneelo control panel, find **SSL** (often under the domain's **Web Services**) and enable the free **Let's Encrypt** certificate for standaction.co.za and www.standaction.co.za. It can take up to an hour. The site is set to always use https once the certificate is active.

## 5. If you use FTP instead of File Manager

Use a free FTP program such as FileZilla. Your FTP host, username and password are in the xneelo control panel (under **FTP**). Connect, open **public_html**, and drag in the **unzipped** contents of the zip (not the zip itself).

## 6. Check it works (5 minutes)

Open these on your phone and computer:

- standaction.co.za: homepage with the new logo and hero
- standaction.co.za/give: opens the campaign page
- Tap **Live pilot** on the homepage: opens at "The Red Dot Process"
- Tap the menu button on a phone, scroll down a page and tap it again: the full menu shows
- Paste standaction.co.za/give into a WhatsApp chat to yourself: the preview shows the smiling ambassador and the headline (WhatsApp sometimes takes a few minutes to pick up a brand-new page)

## Updating the progress bar

The campaign total lives in one tiny file, **progress.txt**, in public_html. It holds just the number of rand raised, for example `82000`.

1. In File Manager, open public_html and click **progress.txt**, then **Edit**.
2. Replace the number with the new total in rand. Digits only: no R, no spaces, no commas.
3. Click **Save**. The bar and the "raised of R150,000" line update for everyone straight away.

Add up SnapScan, EFT, BackaBuddy and GlobalGiving (converted to rand) when you update it. Every few days is plenty, and always after a big day such as GivingTuesday.

## Things that come later

- **GlobalGiving and BackaBuddy links**: send them to Claude. Their buttons switch on in the site files, and you upload the updated files.
- **A 16 Days match**: send the funder's name and amount; the campaign page then shows "Every gift doubled".
