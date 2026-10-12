# Marbled LA seasonal marketing: handoff

Read this first. It covers everything built so far for Thanksgiving 2026 and Holiday 2026,
what's done, what's left, and Tro's rules. Holiday details are in `holiday/PLAN.md`.

## How Tro works
- Direct, terse, plain language. No em-dashes anywhere, in copy or messages.
- Never take his passwords. He signs in himself (browser panel); you take over after.
- Ask before publishing, posting or scheduling anything. Nothing gets scheduled until he approves test emails.
- Send tests to tro@marbled.la.

## Accounts and tools
- Mailchimp: us8 data center, Essentials plan, one audience "Mailer" (list id 362625), about 5,500 subscribed.
  - Essentials can't auto-resend to non-openers or use more than 5 conditions per segment.
  - Merge tags like *|LIST:ADDRESSLINE|* and *|MC:SUBJECT|* only fill in campaign tests and real sends, not template tests.
- Store: order.marbled.la. Thanksgiving menu at /thanksgiving, holiday menu at /holiday.
  Add-to-cart deep links: `?add=<productId>` or `?add=<id1>,<id2>` for bundles. Every link carries
  utm_source=mailchimp, utm_medium=email, utm_campaign=<campaign>, utm_content=<email>-<button>.
- This repo (public) hosts email images. Templates reference them through jsDelivr pinned to a commit:
  `https://cdn.jsdelivr.net/gh/trodersark/marbled-social@<commit>/email/...` (never @main; it caches).

## Audience split (no tags)
Two saved segments in Mailchimp, by email domain. Tro does NOT want existing subscribers tagged.
- "Casual (personal email)": email ends with mail.com, @yahoo.com, @aol.com, @icloud.com or @me.com (3,719 contacts incl. unsubscribed).
- "Corporate (work email)": email does not contain any of those (3,133).
Both segments use all 5 allowed conditions. Excluding buyers needs either a campaign-level exclude
(check if the campaign builder offers it) or dropping the @me.com rule to free a slot.
The 273 contacts imported this week also carry Corporate/Casual tags; ignore those, the segments rule.

## Thanksgiving 2026
Rules:
- Last day to order: noon Mon 11/23. After that, cold pickup only, with reheating instructions,
  pickup Wed 11/25 or Thu 11/26 morning, same online store.
- Office orders: 48 hours' notice, order by noon Mon 11/23, delivery through Wed 11/25.
- Open question for Tro: does "order by the day before pickup" apply to Thanksgiving cold pickup too?
  (It does for Christmas.) If yes, add it to email 11 and its template.

20 Mailchimp templates are built, QA'd and test-sent ("Code your own"; edit at /templates/design?tid=N):
- Home: TG26 Home 01, 02, 03, 04, 05, 06, 07, 09, 10, 11 = tids 10033260 to 10033269 in that order.
- Corporate: TG26 Corp 01 to 10 = tids 10033270 to 10033279.
Source HTML for each is in `templates/`.

Send plan (all Pacific). Each email gets a manual resend to non-openers the next day ("did not open" segment).
Home, to "Casual (personal email)", utm_campaign=thanksgiving-2026:
| Send | Template | Subject | Preview text |
|---|---|---|---|
| Tue 10/13 10am | Home 01 | Thanksgiving, minus the dishes | Three tables for ten, from $345. Add one in a tap. |
| Tue 10/20 10am | Home 02 | The Thanksgiving menu, with notes in the margins | Every dish, a one-line opinion, and an add button. |
| Tue 10/27 10am | Home 04 | The turkey gets the attention. The sides do the work. | Stuffing, mash and gravy in one tap. |
| Tue 11/3 10am | Home 06 | Hot or cold? | Ready to serve Thursday, or chilled with a reheating guide. |
| Sun 11/8 9am | Home 03 | 24, 10, 1, 0 | Hours of brine, people per table, delivery window, pans to scrub. |
| Thu 11/12 10am | Home 05 | 2 weeks until the table | Lock in Thanksgiving now. Orders close noon Mon, Nov 23. |
| Sun 11/15 9am | Home 07 | Leave room for pie | All four pies, one button. |
| Wed 11/18 10am | Home 09 | Carve it or keep it whole | Full turkey, carved, $265. |
| Sun 11/22 9am | Home 10 | The oven's almost full | Thanksgiving orders close Monday at noon. |
| Mon 11/23 2pm | Home 11 | Missed it? Pick it up cold. | The whole menu, cold, with reheating instructions. Pickup Nov 25 or Thanksgiving morning. |
Home 10's resend goes Mon 11/23 7am with subject "Closes at noon today".

Corporate, to "Corporate (work email)", utm_campaign=thanksgiving-2026-corp, all 9am:
| Send | Template | Subject | Preview text |
|---|---|---|---|
| Tue 10/13 | Corp 01 | Thanksgiving for the office, handled | Three spreads for ten, from $345. Delivered hot and on time. |
| Tue 10/20 | Corp 02 | The office Thanksgiving menu, with notes | Every dish, a one-line opinion, and an add button. |
| Tue 10/27 | Corp 03 | The office Thanksgiving, handled | A spread for 20 in one tap. Delivered through Nov 25. |
| Thu 10/29 | Corp 04 | Build the buffet | Half pans that serve 10 to 12. Stuffing, mash and gravy in one tap. |
| Tue 11/3 | Corp 05 | Hot. On time. Ready to serve. | Office lunch that shows up when you said it would. |
| Mon 11/9 | Corp 06 | 24, 10, 1, 0 | Hours of brine, people per spread, the hour you pick, pans to scrub. |
| Thu 11/12 | Corp 07 | 2 weeks until the long weekend | Book the office lunch now. Orders close noon Mon, Nov 23. |
| Mon 11/16 | Corp 08 | Dessert for the team | All four pies, one button. |
| Wed 11/18 | Corp 09 | Carve it or keep it whole | Full turkey, carved, $265. |
| Fri 11/20 | Corp 10 | Last call for the office | Office orders close at noon Mon, Nov 23. Delivery through Wed, Nov 25. |
Corp 10's resend goes Mon 11/23 7am with subject "Office orders close at noon today".

Social (Tro wants Claude to post everything, after his approval):
- Instagram feed post + story the same morning as each Home email; Facebook gets the same feed post.
  Captions are in `social/thanksgiving-captions.txt`. Stories get a link sticker to
  order.marbled.la/thanksgiving?utm_source=instagram&utm_medium=social&utm_campaign=thanksgiving-2026
- Post designs (22 artboards, feed 1080x1350, story 1080x1920) are in a Claude Design canvas from the
  original chat; export them from there.
- Google Business Profile: 5 posts on 10/13, 10/29, 11/12, 11/22 and 11/23 2pm.
- Schedule IG/FB in Meta Business Suite.

Not done yet (Monday 10/12, before Tuesday's first sends):
1. Build the 20 campaigns from the templates (subject, preview text, segment, click tracking, Google Analytics link tracking).
2. Send campaign tests to tro@marbled.la; fix the audience's physical address if it shows wrong.
3. After Tro approves, schedule Tuesday 10/13's two emails (more as he approves the rest).
4. Connect the store so buyers get tagged "Ordered Thanksgiving 2026" and are excluded from later sends.
5. Schedule IG/FB posts and stories and the Google posts.
6. Resends: each day after a send, build a "did not open" resend by hand.

## Holiday 2026
See `holiday/PLAN.md`: 15 emails (9 Home, 6 Corporate), nothing before Mon 11/30. Emails are generated by
`holiday/build.py` with real photos, and are Mailchimp templates (tids 10033280 to 10033294, see PLAN.md).
Left: campaigns, tests, approval. Matching social posts and a team PDF are not started.
