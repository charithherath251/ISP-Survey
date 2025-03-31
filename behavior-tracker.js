(function () {
    let userActivity = {
        mouseMoves: 0,
        keypresses: 0,
        scrolls: 0,
        clicks: 0,
        timing: [],
        startTime: Date.now()
    };

    // Track basic behavior
    document.addEventListener('mousemove', () => userActivity.mouseMoves++);
    document.addEventListener('keydown', () => userActivity.keypresses++);
    document.addEventListener('scroll', () => userActivity.scrolls++);
    document.addEventListener('click', () => userActivity.clicks++);

    document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById('loginForm');
        if (!form) return;

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            // Record total interaction time
            userActivity.timing.push(Date.now() - userActivity.startTime);

            // Send data to FastAPI backend
            fetch('http://127.0.0.1:8001/submit-survey', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userActivity)
            })
                .then(res => res.json())
                .then(data => {
                    alert("✅ Thank you! Your behavior data has been recorded.");
                    form.reset(); // Optional: reset form

                    // Reset activity values for next user
                    userActivity = {
                        mouseMoves: 0,
                        keypresses: 0,
                        scrolls: 0,
                        clicks: 0,
                        timing: [],
                        startTime: Date.now()
                    };
                })
                .catch(err => {
                    console.error("Submission error:", err);
                    alert("⚠️ Error occurred. Please try again.");
                });
        });
    });
})();
