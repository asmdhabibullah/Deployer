# Here's the project plan

1. Create a POST API to archive a PyTorch model using torch-model-archiver and store it in to 'storages' folder.
2.  Create a function to check if a TorchServe instance is already running, and if not, start a new one using the torchserve command.
3. Create a function to check if a model is already registered with the TorchServe instance, and if not, register it using the torch-model-archiver command.
4. Modify the POST API to check if TorchServe is already running, and if not, start a new instance. Then register the new model with TorchServe.
5. Create a GET API to retrieve information on all the running models.
6. Create a Flask Rest API app to get access from NextJS Front-End app.

# Objective:
1. This project is designed to avoid having to use a command line interface, as well as how to easily perform can deploy, and run a PyTorch-trained model after storing it in a project folder 'Storages'.

## CMD
1. Create a model runner file with a .mar extention
```
torch-model-archiver --model-name densenet161 \
--version 1.0 \
--model-file ./image_classifier/densenet_161/model.py \
--serialized-file ./densenet161-8d451a50.pth \ 
--extra-files ./image_classifier/index_to_name.json \
--handler ./image_classifier
```
or
```
torch-model-archiver --model-name test1234 --version 1.0 --serialized-file ./densenet161-8d451a50.pth --model-file ./image_classifier/densenet_161/model.py --handler image_classifier --extra-file ./image_classifier/index_to_name.json
```

2. Start a PyTorch server and attach model with the running server
```
torchserve --start --model-store ./test_models --models test1234=./test_models/test1234.mar
```
or
```
torchserve --start --ncs --ts-config ./config.properties --log-config ./config-logs --model-store ./test_models --models test1234=./test_models/test1234.mar
```


## This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

### Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `pages/index.tsx`. The page auto-updates as you edit the file.

[API routes](https://nextjs.org/docs/api-routes/introduction) can be accessed on [http://localhost:3000/api/hello](http://localhost:3000/api/hello). This endpoint can be edited in `pages/api/hello.ts`.

The `pages/api` directory is mapped to `/api/*`. Files in this directory are treated as [API routes](https://nextjs.org/docs/api-routes/introduction) instead of React pages.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.


### Finally: [যে জীবন মরণেও কাঁদাবে](https://www.youtube.com/watch?v=otQCQ6rLMCg&t=453s&ab_channel=SaifullahMansurOfficial) । সাইফুল্লাহ মানছুর । Je Jibon Moroneo Kadabe । Saifullah Mnasur

```
যে জীবন মরণেও কাঁদাবে,
সে জীবন গড়ে নিও পাড়লে।

যে জীবন মরণেও হাসাবে, 
সে জীবন গড়ে তুমি হারলে।

ক্ষনিকের পৃথিবীতে কখনো,
চিরো দিন কেউ বেঁচে থাকে না।

আফসোস তার তরে যে কভু
মানুষের মনে ছবি আকে না।

হবে তুমি হতো ভাগা বড় যে 
বিদায়ে ও কেউ ক্ষোভ ছাড়লে।

যে জীবন ভালোবাসা পৃথিবীতে 
গেঁথে থাক মানুষের বুকেতে।

সে জীবন কখনো তো মরে না
বেঁচে থাকে মানুষের স্মৃতিতে।।

_ নুরুজ্জামান শাহ

```
