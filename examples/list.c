#include <stdlib.h>

struct ilist {
	int data;
	struct ilist *next;
};

struct ilist *build_list(int *arr, int size)
{
	struct ilist *head = NULL;
	struct ilist *tail;
	struct ilist *node;
	int i;

	for (i = 0; i < size; ++i) {
		node = malloc(sizeof(struct ilist));
		node->data = arr[i];
		node->next = NULL;

		if (!head) {
			head = tail = node;
		} else {
			tail->next = node;
			tail = node;
		}
	}

	return head;
}

int main(void)
{
	int arr[] = { 1, 2, 3, 4 ,5 ,6 ,7, 8, 9, 0};
	__attribute__((unused)) struct ilist *head = build_list(arr, 10);

	return 0;
}
