# Footer Email Signup HTML V2

```
<!--
  ================================================================
  TotalRecalls · Global Footer Email Signup
  ================================================================
  PLACEMENT
    - Sitewide footer only.
    - Sits above the legal links and the copyright line.
    - Appears once per page, after all page content and CTAs.
    - Never placed beside Download free or Buy Pro.

  DESIGN TOKENS
  ----------------------------------------------------------------
  Color
    --tr-obsidian      #111315   Footer background
    --tr-graphite      #1A1D21   Email field fill
    --tr-slate         #2A2F36   Borders, dividers, button border
    --tr-paper         #F3EFE7   Headline, button text, input text
    --tr-mist          #D9D4CB   Description, label, success text
    --tr-dust          #B5AEA3   Privacy line, placeholder text
    --tr-steel-blue    #7A8FA6   Eyebrow, focus ring
    --tr-error         #E3A39A   Error text (muted, not alarm red)

  Typography
    Eyebrow        IBM Plex Mono Medium 12px, uppercase, +0.12em
    Headline       Inter Semibold 24px desktop / 20px mobile, 1.2
    Description    Inter Regular 16px, 1.65 line height, max 560px
    Label          Inter Medium 14px, visible
    Input          Inter Regular 16px (16px prevents iOS zoom)
    Button         Inter Semibold 15px
    Privacy line   Inter Regular 14px (body-sm)
    Messages       Inter Regular 14px

  Shape and Size
    Field and button height   40px
    Radius                    8px
    Border                    1px solid --tr-slate
    Focus                     Steel Blue border + 2px Steel Blue outline,
                              2px offset

  Spacing
    Footer band padding       64px desktop / 48px mobile
    Eyebrow → headline        12px
    Headline → description    12px
    Copy ↔ form (desktop)     48px
    Label → field             8px
    Field ↔ button            8px
    Form → message            8px
    Message → privacy line    12px
    Signup → legal links      48px, separated by a 1px Slate rule

  Layout
    Desktop (≥ 768px)   Copy left, form right, one full-width band
    Mobile (< 768px)    Stacked, field and button full width

  RULES
    - Button uses Secondary style. NEVER Archive Amber.
      Amber is reserved for Download free and Buy Pro.
    - No green success state, no confetti, no icons.
    - No popups, no sticky bars, no exit-intent modals.
  ================================================================
-->

<footer class="site-footer">

  <!-- ===================== EMAIL SIGNUP ===================== -->
  <section class="footer-signup" aria-labelledby="footer-signup-heading">
    <div class="footer-signup__inner">

      <!-- Copy column -->
      <div class="footer-signup__copy">
        <p class="footer-signup__eyebrow">PRODUCT UPDATES</p>

        <h2 id="footer-signup-heading" class="footer-signup__heading">
          Follow what we build next
        </h2>

        <p id="footer-signup-description" class="footer-signup__description">
          Occasional emails about new features, new AI providers, and what's
          coming to TotalRecalls.
        </p>
      </div>

      <!-- Form column -->
      <div class="footer-signup__form-wrap">
        <form
          class="footer-signup__form"
          action="/api/subscribe"
          method="post"
          data-footer-signup
        >
          <label for="footer-signup-email" class="footer-signup__label">
            Email address
          </label>

          <div class="footer-signup__row">
            <input
              id="footer-signup-email"
              class="footer-signup__input"
              type="email"
              name="email"
              placeholder="you@example.com"
              autocomplete="email"
              inputmode="email"
              autocapitalize="off"
              spellcheck="false"
              required
              aria-required="true"
              aria-invalid="false"
              aria-describedby="footer-signup-error footer-signup-privacy"
            />

            <button type="submit" class="footer-signup__button">
              Get updates
            </button>
          </div>

          <!-- Honeypot: off-screen, skipped by keyboard and screen readers -->
          <div class="footer-signup__hp" aria-hidden="true">
            <label for="footer-signup-website">Leave this field empty</label>
            <input
              id="footer-signup-website"
              type="text"
              name="website"
              tabindex="-1"
              autocomplete="off"
            />
          </div>

          <!-- Error message: stays in the DOM, empty until needed -->
          <p
            id="footer-signup-error"
            class="footer-signup__message footer-signup__message--error"
            aria-live="assertive"
            aria-atomic="true"
            data-footer-signup-error
          ></p>
        </form>

        <!-- Success message: live region is always present -->
        <div class="footer-signup__status" role="status" aria-atomic="true">
          <p
            class="footer-signup__message footer-signup__message--success"
            tabindex="-1"
            hidden
            data-footer-signup-success
          >
            You're on the list. Check your inbox to confirm.
          </p>
        </div>

        <p id="footer-signup-privacy" class="footer-signup__privacy">
          Your email is never shared with any third party. Unsubscribe anytime.
        </p>
      </div>

    </div>
  </section>
  <!-- =================== END EMAIL SIGNUP =================== -->

  <!-- Existing legal links go here (Legals, Privacy, Terms) -->
  <!-- Existing copyright line goes here -->
```
