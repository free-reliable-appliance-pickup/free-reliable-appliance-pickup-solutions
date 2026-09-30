export type FaqItem = {
  question: string;
  answer: string;
};

export type LocationPage = {
  slug: string;
  city: string;
  state: string;
  stateCode: string;
  county: string;
  market: string;
  phoneDisplay: string;
  phoneE164: string;
  title: string;
  description: string;
  canonical: string;
  heroImage: string;
  heroImageAlt: string;
  hours: string;
  qualificationSummary: string;
  serviceSummary: string;
  neighborhoods: string[];
  zipCodes: string[];
  applianceLinks: { label: string; href: string }[];
  nearbyLinks: { label: string; href: string }[];
  faqs: FaqItem[];
};

export const locationPages: LocationPage[] = [
  {
    slug: "rancho-cucamonga-appliance-pickup",
    city: "Rancho Cucamonga",
    state: "California",
    stateCode: "CA",
    county: "San Bernardino County",
    market: "Inland Empire",
    phoneDisplay: "909-375-6685",
    phoneE164: "+19093756685",
    title: "Free Appliance Pickup & Removal Rancho Cucamonga CA | Recycling",
    description:
      "Free appliance pickup, removal and recycling in Rancho Cucamonga, CA for qualifying washers, dryers, refrigerators, freezers and stoves. Call/text 909-375-6685.",
    canonical:
      "https://freereliableappliancepickup.com/rancho-cucamonga-appliance-pickup/",
    heroImage:
      "/assets/rancho-cucamonga/rancho-cucamonga-free-appliance-pickup-real-appliance.jpg",
    heroImageAlt:
      "Real appliance for free appliance pickup in Rancho Cucamonga, CA",
    hours: "Mon–Sun 8AM–8PM",
    qualificationSummary:
      "Working and reusable major appliances receive priority. A fully working appliance may qualify, and a mixed load may qualify when approximately 80% of the major appliances work. Pickup is confirmed only after condition, exact address, access and current route availability are reviewed.",
    serviceSummary:
      "Use this page for qualifying refrigerator, freezer, stove, range, oven and mixed major-appliance pickup requests in Rancho Cucamonga. Washer- or dryer-only requests use the dedicated local laundry page.",
    neighborhoods: [
      "Alta Loma",
      "Etiwanda",
      "Victoria",
      "Terra Vista",
      "Haven View Estates"
    ],
    zipCodes: ["91701", "91730", "91737", "91739"],
    applianceLinks: [
      {
        label: "Washer & Dryer Pickup",
        href: "/rancho-cucamonga-washer-dryer-pickup/"
      },
      {
        label: "Refrigerator Pickup",
        href: "/rancho-cucamonga-refrigerator-pickup/"
      },
      {
        label: "Freezer Pickup",
        href: "/rancho-cucamonga-freezer-pickup/"
      },
      {
        label: "Stove & Oven Pickup",
        href: "/rancho-cucamonga-stove-oven-pickup/"
      }
    ],
    nearbyLinks: [
      { label: "Fontana", href: "/fontana-appliance-pickup/" },
      { label: "Upland", href: "/upland-appliance-pickup/" },
      { label: "Ontario", href: "/ontario-appliance-pickup/" }
    ],
    faqs: [
      {
        question: "How much does qualifying appliance pickup cost in Rancho Cucamonga?",
        answer:
          "A qualifying free-route pickup has a $0 pickup charge. Requests that do not qualify may need a municipal, paid-removal or other appropriate option."
      },
      {
        question: "Do I need to put the appliance at the curb?",
        answer:
          "No. Garage, driveway and some inside pickups can be reviewed when access is safe. Send photos and access details before moving the appliance."
      },
      {
        question: "How soon can pickup be arranged?",
        answer:
          "Timing depends on appliance condition, exact address, access and current route availability. Same-day pickup is not guaranteed."
      }
    ]
  }
];

export function getLocationBySlug(slug: string) {
  return locationPages.find((page) => page.slug === slug);
}
