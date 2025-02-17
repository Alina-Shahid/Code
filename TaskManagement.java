import java.io.*;
import java.util.*;

class Task implements Serializable {
    private static final long serialVersionUID = 1L;
    private String title;
    private String description;
    private String dueDate;
    private boolean completed;

    public Task(String title, String description, String dueDate) {
        this.title = title;
        this.description = description;
        this.dueDate = dueDate;
        this.completed = false;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public String getDueDate() {
        return dueDate;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void markCompleted() {
        this.completed = true;
    }

    @Override
    public String toString() {
        return "[" + (completed ? "X" : " ") + "] " + title + " (Due: " + dueDate + ") - " + description;
    }
}

class TaskManager {
    private List<Task> taskList;
    private final String FILE_NAME = "tasks.dat";

    public TaskManager() {
        taskList = new ArrayList<>();
        loadTasks();
    }

    public void addTask(String title, String description, String dueDate) {
        taskList.add(new Task(title, description, dueDate));
        saveTasks();
    }

    public void listTasks() {
        if (taskList.isEmpty()) {
            System.out.println("No tasks available.");
            return;
        }
        for (int i = 0; i < taskList.size(); i++) {
            System.out.println((i + 1) + ". " + taskList.get(i));
        }
    }

    public void markTaskCompleted(int taskIndex) {
        if (taskIndex < 1 || taskIndex > taskList.size()) {
            System.out.println("Invalid task number.");
            return;
        }
        taskList.get(taskIndex - 1).markCompleted();
        saveTasks();
    }

    public void deleteTask(int taskIndex) {
        if (taskIndex < 1 || taskIndex > taskList.size()) {
            System.out.println("Invalid task number.");
            return;
        }
        taskList.remove(taskIndex - 1);
        saveTasks();
    }

    private void saveTasks() {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(FILE_NAME))) {
            oos.writeObject(taskList);
        } catch (IOException e) {
            System.out.println("Error saving tasks: " + e.getMessage());
        }
    }

    private void loadTasks() {
        File file = new File(FILE_NAME);
        if (!file.exists()) return;
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(FILE_NAME))) {
            taskList = (List<Task>) ois.readObject();
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("Error loading tasks: " + e.getMessage());
        }
    }
}

public class TaskManagementSystem {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        TaskManager manager = new TaskManager();

        while (true) {
            System.out.println("\nTask Management System");
            System.out.println("1. Add Task");
            System.out.println("2. View Tasks");
            System.out.println("3. Mark Task as Completed");
            System.out.println("4. Delete Task");
            System.out.println("5. Exit");
            System.out.print("Choose an option: ");
            
            int choice = scanner.nextInt();
            scanner.nextLine(); 
            
            switch (choice) {
                case 1:
                    System.out.print("Enter task title: ");
                    String title = scanner.nextLine();
                    System.out.print("Enter task description: ");
                    String description = scanner.nextLine();
                    System.out.print("Enter due date (YYYY-MM-DD): ");
                    String dueDate = scanner.nextLine();
                    manager.addTask(title, description, dueDate);
                    System.out.println("Task added successfully.");
                    break;
                case 2:
                    manager.listTasks();
                    break;
                case 3:
                    System.out.print("Enter task number to mark as completed: ");
                    int taskNumComplete = scanner.nextInt();
                    manager.markTaskCompleted(taskNumComplete);
                    System.out.println("Task marked as completed.");
                    break;
                case 4:
                    System.out.print("Enter task number to delete: ");
                    int taskNumDelete = scanner.nextInt();
                    manager.deleteTask(taskNumDelete);
                    System.out.println("Task deleted successfully.");
                    break;
                case 5:
                    System.out.println("Exiting Task Management System. Goodbye!");
                    scanner.close();
                    return;
                default:
                    System.out.println("Invalid choice, please try again.");
            }
        }
    }
}
