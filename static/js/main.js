document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("filter-tasks").addEventListener("change", function() {
        var status = this.value;

        var taskCards = document.querySelectorAll(".task-card");
        var doneTasks = document.querySelectorAll(".done-task");

        if (status === "all") {
            taskCards.forEach(card => card.style.display = "block");
        } else if (status === "done") {
            taskCards.forEach(card => card.style.display = "none");
            doneTasks.forEach(card => card.style.display = "block");
        } else if (status === "not-done") {
            taskCards.forEach(card => card.style.display = "block");
            doneTasks.forEach(card => card.style.display = "none");
        }
    });
});
