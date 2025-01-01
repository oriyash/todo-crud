<script setup lang="ts">
import { onMounted, ref } from "vue";
import axios from "axios";

interface Todo {
    id: number;
    body: string;
    done: boolean;
    created_at: string;
}

const todos = ref<Todo[]>([]);
let currentTodoBody: string = "";

onMounted(() => {
    axios.get<Todo[]>("http://localhost:8000/api/todos/fetch/all").then((res) => {
        todos.value.push(...res.data);
    });
});

const handleToggle = (id: number, index: number) => {
    axios.put<Todo>(`http://localhost:8000/api/todos/toggle/${id}`).then((res) => {
        todos.value.splice(index, 1, res.data);
    });
};

const handleDelete = (id: number, index: number) => {
    axios.delete(`http://localhost:8000/api/todos/delete/${id}`).then(() => {
        todos.value.splice(index, 1);
    });
};

const handleAdd = (body: string) => {
    axios
        .post<Todo>("http://localhost:8000/api/todos/insert", { body, done: false })
        .then((res) => {
            todos.value.push(res.data);
            currentTodoBody = "";
        });
};
</script>

<template>
    <h1>Todo App</h1>

    <h2 v-if="!todos.length">No todos to show</h2>
    <div v-else>
        <h2>Todos</h2>

        <p v-for="[index, todo] in todos.entries()" :key="todo.id">
            {{ todo.id }}: {{ todo.body }}, {{ todo.done ? "done" : "not done" }} at
            {{ todo.created_at }}
            <button @click="() => handleToggle(todo.id, index)" style="display: inline">
                toggle
            </button>
            <button @click="() => handleDelete(todo.id, index)" style="display: inline">
                delete
            </button>
        </p>
    </div>

    <div>
        <h2>Add Todo</h2>
        <form @submit.prevent="() => handleAdd(currentTodoBody)">
            <textarea v-model="currentTodoBody"></textarea>
            <br />
            <button type="submit">submit</button>
        </form>
    </div>
</template>

<style scoped></style>
