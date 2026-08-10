function Contact() {
  function handleSubmit(event) {
    event.preventDefault();

    const form = event.currentTarget;

    if (!form.checkValidity()) {
      const root = document.documentElement;
      const previousScrollBehavior = root.style.scrollBehavior;

      root.style.scrollBehavior = "auto";
      form.reportValidity();
      root.style.scrollBehavior = previousScrollBehavior;
      return;
    }

    form.reset();
  }

  return (
    <section id="contact" aria-labelledby="contact-heading">
      <h2 id="contact-heading">Contact Me</h2>

      <form method="post" noValidate onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name</label>
          <input
            id="name"
            name="name"
            type="text"
            required
          />
        </div>

        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            name="email"
            type="email"
            required
          />
        </div>

        <div>
          <label htmlFor="subject">Subject</label>
          <select id="subject" name="subject" required>
            <option value="">Select a subject</option>
            <option value="project">Project Inquiry</option>
            <option value="job">Job Opportunity</option>
            <option value="general">General Question</option>
          </select>
        </div>

        <div>
          <label htmlFor="message">Message</label>
          <textarea
            id="message"
            name="message"
            rows="6"
            minLength={10}
            required
          />
        </div>

        <fieldset>
          <legend>Preferred contact method</legend>

          <div>
            <input
              id="contact-email"
              name="contact-method"
              type="radio"
              value="email"
              defaultChecked
            />
            <label htmlFor="contact-email">Email</label>
          </div>

          <div>
            <input
              id="contact-phone"
              name="contact-method"
              type="radio"
              value="phone"
            />
            <label htmlFor="contact-phone">Phone</label>
          </div>
        </fieldset>

        <div>
          <input
            id="subscribe"
            name="subscribe"
            type="checkbox"
          />
          <label htmlFor="subscribe">
            Subscribe to updates
          </label>
        </div>

        <button type="submit">
          Send Message
        </button>
      </form>
    </section>
  );
}

export default Contact;