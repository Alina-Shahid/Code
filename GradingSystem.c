#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STUDENTS 100
#define MAX_NAME_LENGTH 50

typedef struct {
    char name[MAX_NAME_LENGTH];
    int id;
    float grades[5];
    float average;
} Student;

Student students[MAX_STUDENTS];
int student_count = 0;

void add_student() {
    if (student_count >= MAX_STUDENTS) {
        printf("Maximum student limit reached.\n");
        return;
    }
    
    printf("Enter student name: ");
    scanf(" %[^"]", students[student_count].name);
    printf("Enter student ID: ");
    scanf("%d", &students[student_count].id);
    
    float sum = 0;
    for (int i = 0; i < 5; i++) {
        printf("Enter grade %d: ", i + 1);
        scanf("%f", &students[student_count].grades[i]);
        sum += students[student_count].grades[i];
    }
    
    students[student_count].average = sum / 5.0;
    student_count++;
    printf("Student added successfully!\n");
}

void display_students() {
    if (student_count == 0) {
        printf("No students in the record.\n");
        return;
    }
    
    printf("\nStudent Records:\n");
    for (int i = 0; i < student_count; i++) {
        printf("%d. %s (ID: %d) - Average Grade: %.2f\n", i + 1, students[i].name, students[i].id, students[i].average);
    }
}

void search_student() {
    int id;
    printf("Enter student ID to search: ");
    scanf("%d", &id);
    
    for (int i = 0; i < student_count; i++) {
        if (students[i].id == id) {
            printf("Student Found: %s, ID: %d, Average Grade: %.2f\n", students[i].name, students[i].id, students[i].average);
            return;
        }
    }
    printf("Student not found.\n");
}

void delete_student() {
    int id;
    printf("Enter student ID to delete: ");
    scanf("%d", &id);
    
    for (int i = 0; i < student_count; i++) {
        if (students[i].id == id) {
            for (int j = i; j < student_count - 1; j++) {
                students[j] = students[j + 1];
            }
            student_count--;
            printf("Student deleted successfully.\n");
            return;
        }
    }
    printf("Student not found.\n");
}

void save_to_file() {
    FILE *file = fopen("students.dat", "wb");
    if (!file) {
        printf("Error saving to file.\n");
        return;
    }
    fwrite(&student_count, sizeof(int), 1, file);
    fwrite(students, sizeof(Student), student_count, file);
    fclose(file);
    printf("Data saved successfully.\n");
}

void load_from_file() {
    FILE *file = fopen("students.dat", "rb");
    if (!file) return;
    fread(&student_count, sizeof(int), 1, file);
    fread(students, sizeof(Student), student_count, file);
    fclose(file);
}

int main() {
    load_from_file();
    int choice;
    
    while (1) {
        printf("\nStudent Grade Manager\n");
        printf("1. Add Student\n");
        printf("2. View Students\n");
        printf("3. Search Student\n");
        printf("4. Delete Student\n");
        printf("5. Save & Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                add_student();
                break;
            case 2:
                display_students();
                break;
            case 3:
                search_student();
                break;
            case 4:
                delete_student();
                break;
            case 5:
                save_to_file();
                printf("Exiting...\n");
                return 0;
            default:
                printf("Invalid choice, try again.\n");
        }
    }
}
