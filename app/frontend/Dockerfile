FROM node:20.5.1

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY ./package.json /usr/src/app/

RUN npm i

EXPOSE 3000

CMD ["npm", "run", "dev"]
