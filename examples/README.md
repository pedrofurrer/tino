# Examples

Two fictional projects. Each folder shows the project after one working
session with tino 2.0: the base files (data, notes, sources) plus
everything the installers and rituals wrote. Everything in them is
invented, including the people, the newspaper and the city.

Each session was a sequence of plain requests from the project's owner,
listed below in order. The agent's replies are not included; the files show the state after that
session, reviewed before publication.

## [Los Robles Bakery](bakery/)

1. Set up continuity in this project. I already know what the system is, so
   keep the explanation to a few lines. You have my OK to install it:
   standard scale, working language English. Some history for the logbook:
   we started writing recipes in June 2026 (country loaf and baguette first,
   the seed rye in July), and the sales CSV was set up in June. The
   croissants are our best seller and still have no written recipe. Only ask
   me something if it is truly ambiguous.
2. Now set up metacognition. The defaults are fine: lessons in the repo, the
   index in CLAUDE.md, the three introspection triggers, and always propose
   before filing. You have my OK.
3. Now set up the brain. The parameters: the domain is artisan bread baking
   and running a small bakery; the subdomains are doughs and fermentation,
   baking, costs and pricing, and sales and customers; the validation source
   is notes/bake-log.md plus data/sales-2026.csv; techniques change slowly
   (about 5 years) while prices and costs change fast (about 12 months); the
   context is a neighborhood bakery with two people and a wood-fired oven.
   No landscape layer for now. You have my OK. Do not process the files in
   reading/ yet.
4. Compare the average price of each product in June and in September, and
   tell me which product grew the most in units over the summer.
5. A correction, for the record: the average price of a month must weight
   each weekly price by the units sold that week. A plain mean of the weekly
   prices misleads when volumes change from week to week. If you already did
   it that way, good; either way, propose a judgment lesson from this
   correction.
6. OK, file that lesson.
7. Ingest the two files in reading/ into the brain, with one recommendation
   for each.
8. OK, go ahead with your recommendation for each one.
9. The new mill's flour feels weaker. Should we raise the country loaf's
   hydration to 78 % to make up for it? Answer from the brain and our own
   records.
10. Save progress.

## [Port Alder Courier fact-check desk](fact-check-desk/)

1. Set up continuity in this project. I am the desk's editor and I already
   know what the system is, so keep the explanation to a few lines. You have
   my OK: standard scale, working language English. History for the logbook:
   the desk was set up on 2026-09-08 for the mayoral race; debate 1 was on
   2026-09-10 and the claims log was started that night; data/ was
   downloaded from the city portal on 2026-09-15. Goal: every claim from
   debate 1 verdicted and published before debate 2 on 2026-10-08. Decisions
   already made: verdict drafts live in drafts/, one file per claim (for
   example drafts/C05.md), and the status column of the claims log goes
   unchecked → drafted → in review → published. Only ask me something if it
   is truly ambiguous.
2. Now set up metacognition, with the defaults: lessons in the repo, the
   index in CLAUDE.md, the three introspection triggers, and always propose
   before filing. You have my OK.
3. Now set up the brain. The parameters: the domain is the public record of
   Port Alder for fact-checking the campaign; the subdomains are transit,
   budget and taxes, schools, public works, and libraries; the validation
   source is the city's open data in data/; the field changes fast (treat
   anything older than 12 months as possibly stale, and projections as
   projections); the context is a two-person desk with an editor, publishing
   one verdict per claim, with the same rigor for every candidate. No
   landscape layer. You have my OK. Do not process the files in reading/
   yet.
4. Ingest reading/eastside-blog-schools.md into the brain.
5. OK, go ahead with your recommendation.
6. Now ingest reading/school-facilities-plan-2019-excerpt.md.
7. OK, go ahead with your recommendation.
8. Draft the verdict for claim C05 following style-guide.md, using the brain
   and data/. Show the arithmetic and save the draft where drafts live. Do
   not publish anything; this is a draft for my review.
9. Editor's note, for the record: last week a reporter's draft for C01
   compared the 2026 ridership, which covers only eight months, with full
   years, and it nearly ran. A partial year is not a year. Propose a
   judgment lesson from that correction.
10. OK, file that lesson.
11. Save progress.
