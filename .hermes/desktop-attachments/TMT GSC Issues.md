Conversation with Gemini
I have a problem with the Google Search Console audit of my website (www.topmoneytools.com). The process started weeks ago and it is not moving forward. In the first week of August we did a complete refactoring of the website. We submitted a new Sitemap. The new pages have been discovered but not indexed. What should I do at this point?
When Google Search Console (GSC) shows "Discovered – currently not indexed," it means Google has added your URLs to its queue (likely from your newly submitted sitemap), but Googlebot has not actually fetched or crawled them yet.   

Because you completed a full website refactoring in the first week of August, this delay is fairly common. Google treats major site changes conservatively—it reallocates crawl budget slowly to avoid overloading servers and to evaluate quality signals on newly discovered structures.   

Here is a step-by-step action plan to move things forward:

1. Spot-Test Priority Pages manually
Do not request indexing for every single page (Google will throttle this), but for your 5 to 10 most critical pages (e.g., homepage, top money-making tools/services):

Open GSC and go to the URL Inspection tool.   

Enter the URL and click Test Live URL to confirm Googlebot can fetch the page without errors, noindex tags, or robots.txt blocks.   

If clean, click Request Indexing to bump those priority pages into the queue.   

2. Verify Redirects and Internal Links
Sitemaps inform Google that pages exist, but internal links tell Google which pages matter.   

Clean up redirects: If your URL structure changed during the refactor, ensure 301 redirects go directly from old URLs to new URLs without redirect chains (e.g., A → B, not A → B → C).

Strengthen internal links: Make sure your newly refactored pages are linked directly from your homepage, main navigation, and high-performing blog posts/pages. Avoid "orphaned" pages that only exist in the sitemap.   

3. Audit Staging Directives
It is common during site refactoring for development/staging environments to carry over code that blocks indexing.

Inspect page source code or HTTP response headers to ensure no remnant <meta name="robots" content="noindex"> tags exist on live pages.   

Check your live robots.txt file (e.g., [www.topmoneytools.com/robots.txt](https://www.topmoneytools.com/robots.txt)) to ensure key directories aren't accidentally disallowed.

4. Check Crawl Stats & Server Response Times
Go to Settings > Crawl Stats in GSC:

Look at Average response time (ms). If response times spiked after the refactor, Googlebot will throttle crawling to keep your host stable.   

Check for any 5xx server error spikes or timeout issues.   

Timeline & Expectations:
After a major refactoring, it usually takes 2 to 4 weeks for Google to adjust its crawl frequency and update GSC reports. Since your redesign went live around the first week of August, you are right in that transition window.

Did you change your URL structures or domain/protocol setup during the refactoring, or did the URLs remain exactly the same?

no change to the URL. Just added 30-40 new pages and modified the existing pages. That was a full refactoring job.
Since the URLs remained identical, that rules out broken 301 redirects or lost historical signal paths, which is great news.

However, adding 30–40 new pages alongside a complete rewrite of all existing content is a massive change in the eyes of Google’s algorithms. Google effectively has to re-evaluate the quality, intent, and uniqueness of your entire domain at once.

Here is why it’s stalling and what you should do next:

Why Google Stalls on "Discovered – currently not indexed"
When Google discovers a batch of new/modified pages but doesn't immediately crawl or index them, it is almost always a signal of Crawl Budget & Quality Prioritization:

Low Initial Crawl Priority: Google knows the pages exist (via your new sitemap), but Googlebot doesn't view them as urgent enough to crawl right away compared to the rest of the web.

Content Originality Filters: Finance, money, and affiliate sites (like Top Money Tools) fall into Google’s strict YMYL (Your Money Your Life) category. Google applies extra scrutiny before indexing new financial content to ensure it’s not thin, automated, or duplicated.

Action Plan
1. Build Internal "Signposts" to New Pages
Google relies heavily on internal site architecture to determine which new pages to crawl first.

Link from High-Traffic Pages: Pick your top 5–10 existing pages that do get traffic or are already indexed. Add contextual in-body links pointing directly to your 30–40 new pages.

Update the Homepage / Footer: Add links to new categories or key tools directly on the homepage or in the main navigation menu.

2. Manual URL Inspection Boost
Don't wait for Googlebot to find all 30–40 pages organically.

Take the top 5 most valuable new pages and put them through the GSC URL Inspection Tool.

Click Test Live URL, then click Request Indexing.

Note: Only do this for 3–5 high-priority pages per day. Doing dozens at once won't speed up the queue.

3. Ping External Backlinks / Social Signals
If Googlebot sees new URLs being referenced elsewhere on the web, it prioritizes crawling them immediately:

Share the new pages on your active social channels (LinkedIn, Twitter/X, Pinterest, etc.).

If you send an email newsletter, link to a few of the new pages in your next broadcast to generate real user traffic. Real traffic signals urge Google to index faster.

4. Check Page Speed & Rendering
Since you refactored the site, make sure the new layout hasn't slowed down page loads or created heavy JavaScript rendering blocks.

Run a few new URLs through PageSpeed Insights.

In GSC URL Inspection, check the Rendered HTML to confirm Googlebot can actually read the text content and links on the page (and that content isn't hidden behind unrendered scripts).

Realistic Timeline:
Because you are in the financial/tools niche, it typically takes 2 to 6 weeks for Google to fully crawl, render, evaluate, and index a batch of 30–40 new YMYL pages after a site-wide redesign. Since your launch was in early August, you are currently in the standard waiting window—taking the internal linking steps above will help pull Googlebot through the finish line.

Page indexing
Skip to the latest Gemini result
