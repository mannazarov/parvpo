import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter } from 'k6/metrics';

export let options = {
  stages: [
    { duration: '10s', target: 50 },  // Резкий скачок до 50 пользователей за 10 секунд
    { duration: '30s', target: 50 },  // Поддержание 50 пользователей в течение 30 секунд
    { duration: '10s', target: 0 },    // Постепенное снижение до 0 пользователей за 10 секунд
  ],
};

const BASE_URL = 'http://localhost:5000';
const errors = new Counter('errors');

export default function () {
  // Добавление задачи
  let createRes = http.post(`${BASE_URL}/api/tasks`, JSON.stringify({
    title: `Task ${__ITER}`,
    description: 'This is a test task'
  }), { headers: { 'Content-Type': 'application/json' } });

  check(createRes, {
    'task created': (res) => res.status === 201,
  }) || errors.add(1);

  // Просмотр списка задач
  let listRes = http.get(`${BASE_URL}/api/tasks`);
  check(listRes, {
    'tasks listed': (res) => res.status === 200,
  }) || errors.add(1);

  sleep(1);
}

