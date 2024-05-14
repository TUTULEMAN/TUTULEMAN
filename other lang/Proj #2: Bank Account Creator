#include <stdio.h>
#include <string.h>
#define MAX_ACCOUNTS 100

//structure to represent a bank account
struct account {
    char name[100];
    int account_number;
    float balance;
};
//function to create a new account
void create_account(struct account accounts[], int *num_accounts) {
    struct account new_account;
    printf("Enter the name of the account holder: ");
    scanf("%s", new_account.name);
    printf("Enter the account number: ");
    scanf("%d", &new_account.account_number);
    printf("Enter the initial balance: ");
    scanf("%f", &new_account.balance);
    accounts[*num_accounts] = new_account;
    *num_accounts = *num_accounts + 1;
    printf("Account created successfully!\n");
}
//function to deposit money into an account
void deposit(struct account accounts[], int num_accounts) {
    int account_number;
    float amount;
    printf("Enter the account number: ");
    scanf("%d", &account_number);
    for (int i = 0; i < num_accounts; i++) {
        if (accounts[i].account_number == account_number) {
            printf("Enter the amount to deposit: ");
            scanf("%f", &amount);
            accounts[i].balance += amount;
            printf("Amount deposited successfully!\n");
            return;
        }
    }
    printf("Account not found!\n");
}
//function to withdraw money from an account
void withdraw(struct account accounts[], int num_accounts) {
    int account_number;
    float amount;
    printf("Enter the account number: ");
    scanf("%d", &account_number);
    for (int i = 0; i < num_accounts; i++) {
        if (accounts[i].account_number == account_number) {
            printf("Enter the amount to withdraw: ");
            scanf("%f", &amount);
            if (accounts[i].balance < amount) {
                printf("Insufficient balance!\n");
                return;
            }
            if (amount > 5000) {
                printf("Withdrawal limit exceeded!\n");
                return;
            }
            accounts[i].balance -= amount;
            printf("Amount withdrawn successfully!\n");
            return;
        }
    }
    printf("Account not found!\n");
}
//function to display the account details
void display(struct account accounts[], int num_accounts) {
    int account_number;
    printf("Enter the account number: ");
    scanf("%d", &account_number);
    for (int i = 0; i < num_accounts; i++) {
        if (accounts[i].account_number == account_number) {
            printf("Name: %s\n", accounts[i].name);
            printf("Account number: %d\n", accounts[i].account_number);
            printf("Balance: %.2f\n", accounts[i].balance);
            return;
        }
    }
    printf("Account not found!\n");
}
int main() {
    struct account accounts[MAX_ACCOUNTS];
    int num_accounts = 0;
    int choice;
    while (1) {
        printf("1. Create account\n");
        printf("2. Deposit\n");
        printf("3. Withdraw\n");
        printf("4. Display\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                create_account(accounts, &num_accounts);
                break;
            case 2:
                printf("Enter the account number: ");
                int account_number;
                scanf("%d", &account_number);
                printf("Enter the amount to deposit: ");
                float amount;
                scanf("%f", &amount);
                deposit(accounts, num_accounts);
                break;
            case 3:
                printf("Enter the account number: ");
                scanf("%d", &account_number);
                printf ("Enter the amount to withdraw: ");
                scanf("%f", &amount);
                withdraw(accounts, num_accounts);
                break;
            case 4:
                printf ("Enter the account number: ");
                scanf("%d", &account_number);
                printf("Enter the amount to withdraw: ");
                scanf("%f", &amount);
                display(accounts, num_accounts);
                break;
            case 5:
                printf("Exiting...\n");
                return 0;
            default:
                printf("Invalid choice! Please enter a valid option\n");
        }
    } while (choice != 5)
    return 0;
}
#include <stdlib.h>

//function to delete an account
void delete_account(struct account accounts[], int *num_accounts) {
    int account_number;
    printf("Enter the account number: ");
    scanf("%d", &account_number);
    for (int i = 0; i < *num_accounts; i++) {
        if (accounts[i].account_number == account_number) {
            // shift the remaining accounts to fill the gap
            for (int j = i; j < *num_accounts - 1; j++) {
                accounts[j] = accounts[j + 1];
            }
            *num_accounts = *num_accounts - 1;
            printf("Account deleted successfully!\n");
            return;
        }
    }
    printf("Account not found!\n");
}

//function to calculate the total balance of all accounts
float calculate_total_balance(struct account accounts[], int num_accounts) {
    float total_balance = 0;
    for (int i = 0; i < num_accounts; i++) {
        total_balance += accounts[i].balance;
    }
    return total_balance;
}

//function to find the account with the maximum balance
struct account find_max_balance(struct account accounts[], int num_accounts) {
    struct account max_account = accounts[0];
    for (int i = 1; i < num_accounts; i++) {
        if (accounts[i].balance > max_account.balance) {
            max_account = accounts[i];
        }
    }
    return max_account;
}

//function to find the account with the minimum balance 
struct account find_min_balance(struct account accounts[], int num_accounts) {
    struct account min_account = accounts[0];
    for (int i = 1; i < num_accounts; i++) {
        if (accounts[i].balance < min_account.balance) {
            min_account = accounts[i];
        }
    }
    return min_account;
}

//function to sort the accounts based on the balance in ascending order
void sort_accounts(struct account accounts[], int num_accounts) {
    for (int i = 0; i < num_accounts - 1; i++) {
        for (int j = 0; j < num_accounts - i - 1; j++) {
            if (accounts[j].balance > accounts[j + 1].balance) {
                struct account temp = accounts[j];
                accounts[j] = accounts[j + 1];
                accounts[j + 1] = temp;
            }
        }
    }
}

//function to sort the accounts based on the balance in descending order
void sort_accounts_desc(struct account accounts[], int num_accounts) {
    for (int i = 0; i < num_accounts - 1; i++) {
        for (int j = 0; j < num_accounts - i - 1; j++) {
            if (accounts[j].balance < accounts[j + 1].balance) {
                struct account temp = accounts[j];
                accounts[j] = accounts[j + 1];
                accounts[j + 1] = temp;
            }
        }
    }
}
//function to search for an account by account number
void search_account(struct account accounts[], int num_accounts) {
    int account_number;
    printf("Enter the account number: ");
    scanf("%d", &account_number);
    for (int i = 0; i < num_accounts; i++) {
        if (accounts[i].account_number == account_number) {
            printf("Name: %s\n", accounts[i].name);
            printf("Account number: %d\n", accounts[i].account_number);
            printf("Balance: %.2f\n", accounts[i].balance);
            return;
        }
    }
    printf("Account not found!\n");
}
//function to search for an account by account holder name
void search_account_name(struct account accounts[], int num_accounts) {
    char name[100];
    printf("Enter the name of the account holder: ");
    scanf("%s", name);
    for (int i = 0; i < num_accounts; i++) {
        if (strcmp(accounts[i].name, name) == 0) {
            printf("Name: %s\n", accounts[i].name);
            printf("Account number: %d\n", accounts[i].account_number);
            printf("Balance: %.2f\n", accounts[i].balance);
            return;
        }
    }
    printf("Account not found!\n");
}
//function to update the account details
void update_account(struct account accounts[], int num_accounts) {
    int account_number;
    printf("Enter the account number: ");
    scanf("%d", &account_number);
    for (int i = 0; i < num_accounts; i++) {
        if (accounts[i].account_number == account_number) {
            printf("Enter the new name of the account holder: ");
            scanf("%s", accounts[i].name);
            printf("Enter the new account number: ");
            scanf("%d", &accounts[i].account_number);
            printf("Enter the new balance: ");
            scanf("%f", &accounts[i].balance);
            printf("Account details updated successfully!\n");
            return;
        }
    }
    printf("Account not found!\n");
}
//function to display all accounts
void display_all(struct account accounts[], int num_accounts) {
    for (int i = 0; i < num_accounts; i++) {
        printf("Name: %s\n", accounts[i].name);
        printf("Account number: %d\n", accounts[i].account_number);
        printf("Balance: %.2f\n", accounts[i].balance);
    }
}
//function to display the menu
void display_menu() {
    printf("1. Create account\n");
    printf("2. Deposit\n");
    printf("3. Withdraw\n");
    printf("4. Display\n");
    printf("5. Delete account\n");
    printf("6. Calculate total balance\n");
    printf("7. Find account with maximum balance\n");
    printf("8. Find account with minimum balance\n");
    printf("9. Sort accounts based on balance in ascending order\n");
    printf("10. Sort accounts based on balance in descending order\n");
    printf("11. Search account by account number\n");
    printf("12. Search account by account holder name\n");
    printf("13. Update account details\n");
    printf("14. Display all accounts\n");
    printf("15. Exit\n");
}
int main() {
    struct account accounts[MAX_ACCOUNTS];
    int num_accounts = 0;
    int choice;
    while (1) {
        display_menu();
        printf("Enter your choice: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                create_account(accounts, &num_accounts);
                break;
            case 2:
                deposit(accounts, num_accounts);
                break;
            case 3:
                withdraw(accounts, num_accounts);
                break;
            case 4:
                display(accounts, num_accounts);
                break;
            case 5:
                delete_account(accounts, &num_accounts);
                break;
            case 6:
                printf("Total balance: %.2f\n", calculate_total_balance(accounts, num_accounts));
                break;
            case 7:
                struct account max_account = find_max_balance(accounts, num_accounts);
                printf("Account with maximum balance:\n");
                printf("Name: %s\n", max_account.name);
                printf("Account number: %d\n", max_account.account_number);
                printf("Balance: %.2f\n", max_account.balance);
                break;
            case 8:
                struct account min_account = find_min_balance(accounts, num_accounts);
                printf("Account with minimum balance:\n");
                printf("Name: %s\n", min_account.name);
                printf("Account number: %d\n", min_account.account_number);
                printf("Balance: %.2f\n", min_account.balance);
                break;
            case 9:
                sort_accounts(accounts, num_accounts);
                printf("Accounts sorted based on balance in ascending order!\n");
                break;
            case 10:
                sort_accounts_desc(accounts, num_accounts);
                printf("Accounts sorted based on balance in descending order!\n");
                break;
            case 11:
                search_account(accounts, num_accounts);
                break;
            case 12:
                search_account_name(accounts, num_accounts);
                break;
            case 13:
                update_account(accounts, num_accounts);
                break;
            case 14:
                display_all(accounts, num_accounts);
                break;
            case 15:
                printf("Exiting...\n");
                return 0;
            default:
                printf("Invalid choice! Please enter a valid option\n");
        }
    }
    return 0;
}
