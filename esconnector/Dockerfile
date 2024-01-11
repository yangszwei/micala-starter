FROM node:20-alpine
WORKDIR /app

# Install git
RUN apk add --no-cache git

# Clone the esconnector repo and remove sample data
RUN git clone https://github.com/zhr85210078/node-mongodb-es-connector.git /app && \
    cd /app && \
    rm -rf crawlerData

# Install dependencies
RUN npm install

# Copy the config file
COPY ./crawlerData /app/crawlerData

CMD ["node", "app.js"]
