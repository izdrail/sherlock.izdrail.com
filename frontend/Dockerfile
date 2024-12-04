# This is the older version!

FROM node:22-alpine

WORKDIR /app

COPY . .

RUN npm install


RUN npm run build

EXPOSE 8000
#vite --host 127.0.0.1 --port 8000
CMD ["npx", "vite", "--host", "0.0.0.0", "--port", "8000"]
