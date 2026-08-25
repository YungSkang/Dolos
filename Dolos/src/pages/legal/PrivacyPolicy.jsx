export default function PrivacyPolicy() {
  return (
    <div className="legal-page">
      <h1>Privacy Policy - Dolos</h1>
      <p><em>Last updated: 25/08/2026</em></p>

      <p>
        Dolos ("we," "our," "the Service") is an educational cybersecurity
        awareness tool available at{" "}
        <a href="https://dolos-nu.vercel.app">dolos-nu.vercel.app</a>. This
        policy explains what data the current version of Dolos (the password
        strength checker) processes, why, and your rights over it.
      </p>

      <h2>1. Who is responsible for this data</h2>
      <p>
        Dolos is operated by Angelos Skandalis, an individual developer based
        in Greece, as a personal/portfolio project.
      </p>
      <p>Contact: skandalesa@gmail.com</p>

      <h2>2. What data we process</h2>
      <p>The current version of Dolos offers:</p>
      <ul>
        <li>
          <strong>Password Strength Analysis</strong> - you enter a password
          (or a candidate password) and we calculate its entropy, strength
          rating, and estimated crack time.
        </li>
        <li>
          <strong>Personal Info Attack Simulator</strong> - you may optionally
          enter a first name, last name, birthdate, pet name, and/or city.
          This is used to generate example passwords an attacker could guess
          from that information, purely for demonstration purposes.
        </li>
        <li>
          <strong>Secure Password Generator</strong> — runs entirely in your
          browser using the Web Crypto API. This data never leaves your
          device and is never sent to us.
        </li>
      </ul>
      <p>
        Any password or personal information you submit to the analysis or
        simulator features is sent to our backend server to perform the
        calculation, is used only for that single request, and{" "}
        <strong>
          is not stored, logged to a database, or retained
        </strong>{" "}
        after the response is returned to you.
      </p>

      <h2>3. Why we process this data</h2>
      <ul>
        <li>
          <strong>Legal basis:</strong> Consent (Art. 6(1)(a) GDPR).
          Submitting information into the analyzer or simulator is entirely
          optional and is treated as your consent to that one-time
          processing.
        </li>
        <li>
          <strong>Purpose:</strong> To provide the educational demonstration
          you requested (showing password strength or attacker-guessable
          variants).
        </li>
      </ul>

      <h2>4. Retention</h2>
      <p>
        We do not retain the content of your submissions. Once your request
        is processed and the result is returned to your browser, the input
        data is discarded and not written to any database.
      </p>
      <p>
        Note: our hosting providers (see below) may generate short-lived
        technical server logs (e.g., IP address, timestamp, request path) for
        security and operational purposes, independent of the analysis
        content itself. These are governed by the providers' own retention
        practices.
      </p>

      <h2>5. Third parties / sub-processors</h2>
      <table>
        <thead>
          <tr>
            <th>Provider</th>
            <th>Role</th>
            <th>Data involved</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Vercel</td>
            <td>Hosts the frontend (website you're viewing)</td>
            <td>Standard web request metadata (IP, browser info)</td>
          </tr>
          <tr>
            <td>Render</td>
            <td>Hosts the backend API that performs the analysis</td>
            <td>
              Request metadata; the password/personal-info payload transits
              through it but is not stored
            </td>
          </tr>
        </tbody>
      </table>
      <p>
        We do not sell, share, or use your data for advertising, profiling,
        or analytics.
      </p>

      <h2>6. International data transfers</h2>
      <p>
        Vercel and Render may process technical logs on infrastructure
        located outside Greece/the EU (e.g., the US). Where this occurs, it
        relies on the providers' own GDPR-compliant transfer mechanisms
        (e.g., Standard Contractual Clauses).
      </p>

      <h2>7. Your rights (GDPR)</h2>
      <p>
        Because nothing you submit is stored, most storage-dependent rights
        (e.g., erasure of a stored record) don't apply in practice - there is
        no persistent record to erase or export. You still have the right
        to:
      </p>
      <ul>
        <li>Ask us what data, if any, is processed about you</li>
        <li>Object to processing</li>
        <li>
          Lodge a complaint with your national Data Protection Authority (in
          Greece: the{" "}
          <a href="https://www.dpa.gr">Hellenic Data Protection Authority</a>
          )
        </li>
      </ul>
      <p>Contact us at skandalesa@gmail.com with any request.</p>

      <h2>8. Children</h2>
      <p>
        Dolos is not directed at children and is not intended for use by
        anyone under 16.
      </p>

      <h2>9. Changes to this policy</h2>
      <p>
        We may update this policy as the Service evolves (e.g., if future
        versions add URL scanning via third-party threat-intelligence APIs,
        this policy will be updated to disclose that before it goes live).
        Material changes will be reflected here with an updated "Last
        updated" date.
      </p>
    </div>
  );
}