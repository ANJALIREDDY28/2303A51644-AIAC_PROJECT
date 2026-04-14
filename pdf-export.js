// PDF Export functionality using jsPDF
function downloadPDF() {
    if (!window.currentPlan) {
        alert('Please generate a plan first!');
        return;
    }
    
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Header
    doc.setFontSize(24);
    doc.setFont(undefined, 'bold');
    doc.text('Your Personalized Diet Plan', 20, 30);
    
    doc.setFontSize(14);
    doc.setFont(undefined, 'normal');
    doc.text(`Generated for ${document.getElementById('user-info').textContent}`, 20, 45);
    doc.text(`Date: ${new Date().toLocaleDateString()}`, 20, 55);
    
    // Metrics
    doc.setFontSize(12);
    doc.text('📊 Health Metrics:', 20, 75);
    doc.text(`BMI: ${window.currentPlan.bmi}`, 30, 90);
    doc.text(`Daily Calories: ${window.currentPlan.daily_calories.toLocaleString()} kcal`, 30, 100);
    doc.text(`Water Intake: ${window.currentPlan.water_intake}`, 30, 110);
    
    // Meals
    const meals = [
        { title: '🍳 Breakfast', content: window.currentPlan.breakfast },
        { title: '🍛 Lunch', content: window.currentPlan.lunch },
        { title: '🍽️ Dinner', content: window.currentPlan.dinner },
        { title: '🥜 Snacks', content: window.currentPlan.snacks }
    ];
    
    let yPos = 140;
    meals.forEach(meal => {
        doc.setFont(undefined, 'bold');
        doc.text(meal.title, 20, yPos);
        doc.setFont(undefined, 'normal');
        doc.text(meal.content, 20, yPos + 10);
        yPos += 30;
    });
    
    // Footer tips
    doc.setFontSize(10);
    doc.text('💡 Tips: Stay consistent, drink water throughout the day, combine with exercise!', 20, yPos + 10);
    
    // Save
    doc.save('diet-plan.pdf');
}

// Attach to global scope
window.downloadPDF = downloadPDF;

// Wire up button
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('download-pdf');
    if (btn) {
        btn.addEventListener('click', downloadPDF);
    }
});

