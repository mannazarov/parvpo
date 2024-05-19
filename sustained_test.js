import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter } from 'k6/metrics';

export let options = {
  stages: [
    { duration: '2m', target: 10 },   // Постепенное увеличение до 10 пользователей за 2 минуты
    { duration: '3m', target: 10 },   // Поддержание 10 пользователей в течение 3 минут
    { duration: '2m', target: 0 },    // Постепенное снижение до 0 пользователей за 2 минуты
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

