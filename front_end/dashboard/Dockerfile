FROM node:19-buster
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
EXPOSE 3000
CMD HOST=0.0.0.0 npm start
