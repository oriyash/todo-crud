<script setup lang="ts">
import { onMounted, ref } from "vue";
import axios from "axios";
import type { Todo } from "./types/Todo";

const todos = ref<Todo[]>([]);
const editing = ref<number | null>(null);
let currentTodoBody: string = "";
let currentEditValue: string = "";

onMounted(() => {
    axios.get<Todo[]>("/api/todos/fetch/all").then((res) => {
        todos.value.push(...res.data);
    });
});

const handleToggle = (id: number, index: number) => {
    axios.put<Todo>(`/api/todos/toggle/${id}`).then((res) => {
        todos.value.splice(index, 1, res.data);
    });
};

const handleDelete = (id: number, index: number) => {
    axios.delete(`/api/todos/delete/${id}`).then(() => {
        todos.value.splice(index, 1);
    });
};

const handleAdd = (body: string) => {
    const cleanBody: string = body.trim();

    if (cleanBody === "") {
        return;
    }

    axios.post<Todo>("/api/todos/insert", { body: cleanBody, done: false }).then((res) => {
        todos.value.push(res.data);
        currentTodoBody = "";
    });
};

const handleClear = () => {
    axios.delete("/api/todos/delete/all").then(() => {
        todos.value = [];
    });
};

const handleEdit = (id: number, body: string, index: number) => {
    const cleanBody: string = body.trim();

    if (cleanBody === "") {
        return;
    }

    axios.put<Todo>(`/api/todos/edit/${id}`, { body: cleanBody }).then((res) => {
        todos.value.splice(index, 1, res.data);
        editing.value = null;
        currentEditValue = "";
    });
};

const handleEditClick = (body: string, index: number) => {
    editing.value = index;
    currentEditValue = body;
};
</script>

<template>
    <h1>Todo App</h1>

    <h2 v-if="!todos.length">No todos to show</h2>
    <div v-else>
        <h2>Todos</h2>

        <button @click.prevent="handleClear">Clear All</button>

        <p v-for="[index, todo] in todos.entries()" :key="todo.id">
            <input
                type="checkbox"
                style="display: inline"
                v-model="todo.done"
                @change.prevent="() => handleToggle(todo.id, index)"
            />
            {{ todo.id }}: <span v-if="editing !== index">{{ todo.body }} - </span
            ><input
                v-else
                type="text"
                style="display: inline"
                v-model="currentEditValue"
                @keyup.enter="() => handleEdit(todo.id, currentEditValue, index)"
            />
            created at
            {{ todo.created_at }}
            <button
                v-if="editing !== index"
                @click="() => handleDelete(todo.id, index)"
                style="display: inline"
            >
                delete
            </button>
            <button
                v-if="editing !== index"
                style="display: inline"
                @click.prevent="() => handleEditClick(todo.body, index)"
            >
                edit
            </button>
        </p>
    </div>

    <div>
        <h2>Add Todo</h2>
        <form @submit.prevent="() => handleAdd(currentTodoBody)">
            <input
                type="text"
                v-model="currentTodoBody"
                @keyup.enter="() => handleAdd(currentTodoBody)"
            />
            <br />
            <button type="submit">submit</button>
        </form>
    </div>
</template>

<style scoped></style>
