function addTask() {
    let input = document.getElementById("taskInput");
    let text = input.value;

    if (text.trim() === "") {
        return;
    }
    let taskDiv = document.createElement("div");
    taskDiv.classList.add("task");

    let taskText = document.createElement("p");
    taskText.innerText = text;

    let completeBtn = document.createElement("button");
    completeBtn.innerText = "Completed";

    completeBtn.onclick = function () {
        completeBtn.classList.add("completed");
    }

    let removeBtn = document.createElement("button");
    removeBtn.innerText = "remove";
    removeBtn.classList.add("remove");
    
    removeBtn.onclick=function(){
        taskDiv.remove();
    }

      taskDiv.appendChild(taskText);
      taskDiv.appendChild(completeBtn);
      taskDiv.appendChild(removeBtn);

      document.getElementById("task-container").appendChild(taskDiv);
      input.value = "";
    

}
