# Partner dispatch: prevent wasted appliance pickup trips
Updated: October 10, 2026. Owner: Free Reliable Appliance Pickup.
Operational checklist; this does **not** imply any automated dispatch hold exists in Formspree or that a machine was independently inspected.

## Why this exists
A customer may call a washing machine "working" because the motor turns or it spins, while loud rumbling/grinding indicates a likely mechanical problem (e.g., bearing). If a partner drives a long distance expecting a fully operational appliance, everybody loses time and fuel. Never equate "powers on" with "fully working."

## Required checks before asking a partner to travel
1. Read all submitted fields: `condition`, `condition_details`, `laundry_cycle_test`, `laundry_unusual_noise`, `laundry_condition_attestation`, `Dispatch Condition Gate`, `appliance`, and access details. An omitted field means not verified, not a pass.
2. For **washer**: ask whether a complete wash and spin cycle finished normally, whether loud rumbling/grinding/banging/shaking occurred, whether it leaks, and whether error codes appear. For **dryer**: ask whether a complete drying/heating cycle worked normally, with no loud noises or overheating. For **refrigerator**: verify *actual cooling*, not merely power/lights. For **stove/range**: verify burners and oven operation safely, without asking a customer to perform hazardous tests.
3. If the customer selected "Fully Working" but says loud noise, unusual vibration, leaks, no heat/cooling, or incomplete cycle: **correct the condition to "Works, but has problems" or "Needs repair"** before offering the lead. Do not promise free pickup for an individual broken machine. Mixed loads may be reviewed when about 80% of the major appliances are working.
4. For distant trips or uncertain washing-machine reports, request recent clear photos and (if safe and practical) a brief operating/spin-cycle video. Never ask a customer to run an appliance that may be unsafe. Photos/videos reduce risk but do not prove a hidden mechanical issue is absent.
5. Tell the pickup partner the reported condition and any noise/leaks **before** they accept the trip. Get explicit partner acceptance and communicate any qualification/coverage limits to the customer. Record the operator's acceptance and agreed plan; do not silently relabel damaged appliances as working.
6. Verify the actual address, floor, stairs, gates, access, distance and appliance type before dispatch. Confirm time with both customer and partner. No pickup is guaranteed until the customer qualification and local coverage review are complete.
7. If the pickup turns out materially different from the customer's description: stop, review options with the partner and customer, and do not pressure the partner into accepting it for free.

## New online Formspree intake
The shared `assets/customer-routing.js` inserts two **required** laundry answers ("full cycle tested?" and "unusual grinding/rumbling/banging/shaking?") plus a condition-disclosure attestation when the selected appliance includes a washer/dryer. It prevents contradictory "Fully Working" answers with browser validation, and requires the written problem explanation for known issues. The form request includes `Dispatch Condition Gate`, `Customer Laundry Cycle Test`, `Customer Reported Unusual Noise`, and `Customer Defect Explanation` as plain metadata.

**Important:** This is a review flag in a submitted form, not an integrated dispatch stop or independent verification. A person handling partner assignments **must inspect it before offering a trip**. The answers can still be mistaken or dishonest. An untested unit is not "fully working" merely because it starts.

## Customer confirmation questions (phone/text)
"Before we send someone, did the washer complete a full wash and spin cycle, without loud rumbling, grinding, banging, strong shaking or leaking? If it makes any unusual noise, please tell us now. Does it have any error codes? A machine that just turns on is not the same as fully working. Photos or a short safe spin video would help us review it."

## Metrics to track
Capture wasted trips caused by inaccurate condition, travel miles/time, category, failure reason, whether cycle/noise questions were answered, and whether the customer submitted media. Compare rate of mismatched-condition trips after this change. Don't equate more submissions with better-quality leads.
