import Nav from "@/components/landing/Nav";
import ThreatFeed from "@/components/landing/ThreatFeed";
import SentinelHero from "@/components/landing/SentinelHero";
import ResolutionPath from "@/components/landing/ResolutionPath";
import RiskMatrix from "@/components/landing/RiskMatrix";
import LibraryPreview from "@/components/landing/LibraryPreview";
import Guides from "@/components/landing/Guides";
import PricingSection from "@/components/landing/PricingSection";
import SiteFooter from "@/components/landing/SiteFooter";

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <ThreatFeed />
      <Nav />
      <SentinelHero />
      <ResolutionPath />
      <RiskMatrix />
      <LibraryPreview />
      <Guides />
      <PricingSection />
      <SiteFooter />
    </div>
  );
}