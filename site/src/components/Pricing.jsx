import { Section } from "./ui/Section";
import { SectionTitle } from "./ui/SectionTitle";
import { ButtonPrimary } from "./ui/ButtonPrimary";

export default function Pricing() {
  return (
    <Section id="pricing" bg="white">
      <div className="text-center space-y-6">
        <SectionTitle>Pricing</SectionTitle>
        <div className="text-4xl font-semibold">$24 launch price</div>
        <div className="text-gray-600">One-time purchase · Windows app · Local files only</div>
        <ButtonPrimary href="#buy">Buy TotalRecalls — $24</ButtonPrimary>
      </div>
    </Section>
  );
}
