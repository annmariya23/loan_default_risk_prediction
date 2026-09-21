document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("riskForm");

    if (!form) {
        console.error("riskForm not found");
        return;
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        // ============================
        // GET INPUT VALUES
        // ============================

        const loan = Number(document.querySelector('[name="loan_amnt"]').value) || 0;
        const funded = Number(document.querySelector('[name="funded_amnt"]').value) || 0;
        const investor = Number(document.querySelector('[name="funded_amnt_inv"]').value) || 0;
        const interest = Number(document.querySelector('[name="int_rate"]').value) || 0;
        const installment = Number(document.querySelector('[name="installment"]').value) || 0;

        const income = Number(document.querySelector('[name="annual_inc"]').value) || 0;
        const dti = Number(document.querySelector('[name="dti"]').value) || 0;
        const revolBal = Number(document.querySelector('[name="revol_bal"]').value) || 0;
        const revolUtil = Number(document.querySelector('[name="revol_util"]').value) || 0;

        const delinq = Number(document.querySelector('[name="delinq_2yrs"]').value) || 0;
        const inquiries = Number(document.querySelector('[name="inq_last_6mths"]').value) || 0;
        const openAcc = Number(document.querySelector('[name="open_acc"]').value) || 0;
        const totalAcc = Number(document.querySelector('[name="total_acc"]').value) || 0;
        const mortAcc = Number(document.querySelector('[name="mort_acc"]').value) || 0;
        const pubRec = Number(document.querySelector('[name="pub_rec"]').value) || 0;
        const bankruptcies = Number(document.querySelector('[name="pub_rec_bankruptcies"]').value) || 0;


        // ============================
        // SIMPLE RISK CALCULATION
        // ============================
        // This is a browser-side demonstration score.
        // It is NOT the saved Spark ML model.

        let risk = 2;

        // Interest rate
        risk += interest * 0.40;

        // Debt-to-income
        risk += dti * 0.28;

        // Revolving utilisation
        risk += revolUtil * 0.10;

        // Delinquencies
        risk += delinq * 3.0;

        // Recent enquiries
        risk += inquiries * 1.0;

        // Public records
        risk += pubRec * 2.0;

        // Bankruptcies
        risk += bankruptcies * 3.0;

        // Loan-to-income pressure
        if (income > 0) {
            const loanIncomeRatio = (loan / income) * 100;

            if (loanIncomeRatio > 15) {
                risk += (loanIncomeRatio - 15) * 0.15;
            }
        }

        // Very high utilisation
        if (revolUtil > 70) {
            risk += 5;
        }

        // Multiple delinquencies
        if (delinq >= 2) {
            risk += 5;
        }

        // Keep between 1 and 99
        risk = Math.max(1, Math.min(99, risk));

        // Round
        risk = Math.round(risk * 10) / 10;


        // ============================
        // CLASSIFICATION
        // ============================

        let prediction;
        let label;
        let icon;

        if (risk >= 50) {
            prediction = "Default (1)";
            label = "High Risk";
            icon = "!";
        } else {
            prediction = "Non-default (0)";
            label = "Low Risk";
            icon = "✓";
        }


        // ============================
        // UPDATE RESULT CARD
        // ============================

        document.getElementById("score").textContent = risk + "%";

        document.getElementById("riskBar").style.width = risk + "%";

        document.getElementById("riskLabel").textContent = label;

        document.getElementById("predictionValue").textContent = prediction;

        document.getElementById("resultIcon").textContent = icon;


        // ============================
        // RESULT MESSAGE
        // ============================

        const resultText = document.getElementById("resultText");

        if (risk >= 50) {
            resultText.innerHTML =
                "The applicant has a <strong>higher estimated risk</strong> of loan default.";
        } else {
            resultText.innerHTML =
                "The applicant has a <strong>lower estimated risk</strong> of loan default.";
        }


        // ============================
        // UPDATE SUMMARY
        // ============================

        document.getElementById("summaryLoan").textContent =
            "$" + loan.toLocaleString();

        document.getElementById("summaryIncome").textContent =
            "$" + income.toLocaleString();

        document.getElementById("summaryDti").textContent =
            dti + "%";

        document.getElementById("summaryRate").textContent =
            interest + "%";


        // ============================
        // CHANGE RESULT COLORS
        // ============================

        const resultBox = document.getElementById("resultBox");

        if (risk >= 50) {
            resultBox.classList.remove("low");
            resultBox.classList.add("high");

            document.getElementById("riskLabel").style.color = "#e77b72";
            document.getElementById("score").style.color = "#e77b72";
            document.getElementById("riskBar").style.background = "#e77b72";

        } else {
            resultBox.classList.remove("high");
            resultBox.classList.add("low");

            document.getElementById("riskLabel").style.color = "#65d2bf";
            document.getElementById("score").style.color = "#55c8bd";
            document.getElementById("riskBar").style.background = "#58c7bd";
        }

    });


    // ============================
    // UPDATE SUMMARY WHILE TYPING
    // ============================

    function updateSummary() {

        const loan =
            Number(document.querySelector('[name="loan_amnt"]').value) || 0;

        const income =
            Number(document.querySelector('[name="annual_inc"]').value) || 0;

        const dti =
            Number(document.querySelector('[name="dti"]').value) || 0;

        const interest =
            Number(document.querySelector('[name="int_rate"]').value) || 0;

        document.getElementById("summaryLoan").textContent =
            "$" + loan.toLocaleString();

        document.getElementById("summaryIncome").textContent =
            "$" + income.toLocaleString();

        document.getElementById("summaryDti").textContent =
            dti + "%";

        document.getElementById("summaryRate").textContent =
            interest + "%";
    }


    // Listen to all inputs
    const inputs = form.querySelectorAll("input");

    inputs.forEach(function (input) {
        input.addEventListener("input", updateSummary);
    });

});