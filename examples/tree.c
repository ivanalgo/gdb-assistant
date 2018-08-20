#include <stdlib.h>

struct btree {
	int data;
	struct btree *left;
	struct btree *right;
};

void insert_tree(struct btree **root, int data)
{
	struct btree **inserted;
	struct btree *node = malloc(sizeof(struct btree));
	node->data = data;
	node->left = node->right = NULL;

	if (!(*root)) {
		*root = node;
		return;
	}

	inserted = &(*root);
	while (*inserted) {
		if (data <= (*inserted)->data)
			inserted = &(*inserted)->left;
		else
			inserted = &(*inserted)->right;
	}

	*inserted = node;
}

struct btree *build_tree(int *arr, int size)
{
	struct btree *tree = NULL;
	int i;

	for (i = 0; i < size; ++i) {
		insert_tree(&tree, arr[i]);
	}

	return tree;
}

int main()
{
	int arr[] = {1, 3, 5, 7, 9, 0, 8, 6, 4, 2};
	__attribute__((unused)) struct btree *tree = build_tree(arr, 10);

	return 0;
}
