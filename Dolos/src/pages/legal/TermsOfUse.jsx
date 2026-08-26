export default function TermsOfUse() {
  return (
    <div className="legal-page">
      <h1>Terms of Use -     Dolos</h1>
      <p><em>Last updated: 25/08/2026</em></p>

      <p>
        Please read these Terms of Use ("Terms") before using Dolos (the
        "Service"), available at{" "}
        <a href="https://dolos-nu.vercel.app">dolos-nu.vercel.app</a>. By
        using the Service, you agree to these Terms.
      </p>

      <h2>1. What Dolos is</h2>
      <p>
        Dolos is an educational tool that demonstrates cybersecurity
        concepts, including password strength, entropy, and how attackers
        construct targeted password guesses from personal information (name,
        birthdate, pet name, city). It is provided{" "}
        <strong>for educational and awareness purposes only</strong>.
      </p>

      <h2>2. Acceptable use</h2>
      <p>You agree to use Dolos only:</p>
      <ul>
        <li>
          On passwords and personal information{" "}
          <strong>you own or have explicit permission to test</strong> (e.g.,
          your own accounts, or with the informed consent of the person whose
          information you're using).
        </li>
        <li>For learning, research, or awareness purposes.</li>
      </ul>
      <p>You agree <strong>not</strong> to use Dolos to:</p>
      <ul>
        <li>
          Analyze, guess, or attempt to compromise credentials belonging to
          another person without their consent.
        </li>
        <li>
          Attempt to use outputs from the Service (e.g., generated candidate
          passwords) to gain unauthorized access to any account or system.
        </li>
        <li>
          Reverse-engineer, scrape, or overload the Service's infrastructure.
        </li>
      </ul>

      <h2>3. No warranty</h2>
      <p>
        The Service is provided "as is," without warranties of any kind.
        Strength ratings, crack-time estimates, and generated candidates are
        illustrative approximations based on published benchmarks (e.g.,
        Hashcat, Hive Systems) and <strong>do not guarantee</strong> the
        real-world security or vulnerability of any password.
      </p>

      <h2>4. Limitation of liability</h2>
      <p>
        To the maximum extent permitted by law, Angelos Skandalis is not
        liable for any damages arising from your use or misuse of the
        Service, including any loss resulting from reliance on its output or
        from using it against a third party without consent.
      </p>

      <h2>5. Data submitted to the Service</h2>
      <p>
        By submitting a password or personal details into the analyzer, you
        confirm you have the right to do so. See our{" "}
        <a href="/privacy">Privacy Policy</a> for how that data is handled —
        in short, it's used only to generate your result and is not stored.
      </p>

      <h2>6. Intellectual property</h2>
      <p>
        The Dolos source code is released under the MIT License (see the
        project's GitHub repository). The Service's branding, name, and
        design are otherwise the property of Angelos Skandalis.
      </p>

      <h2>7. Changes</h2>
      <p>
        These Terms may be updated as the Service evolves. Continued use
        after changes are posted constitutes acceptance of the revised
        Terms.
      </p>

      <h2>8. Governing law</h2>
      <p>
        These Terms are governed by the laws of Greece, without regard to
        conflict-of-law principles.
      </p>

      <h2>9. Contact</h2>
      <p>Questions about these Terms: skandalesa@gmail.com</p>
    </div>
  );
}