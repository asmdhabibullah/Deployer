import Link from "next/link";
import useSWR, { } from "swr";
import { fetcher } from "@/utils";

export interface ModelsProps {
  models?: object[]
}

const Models = ({ models }: ModelsProps) => {

  const { data, error } = useSWR('http://127.0.0.1:3520/api/v1/model', fetcher)


  console.log("data", data);


  if (!error && data) {
    return (
      <div className="bg-[#0b163d] w-[auto] h-[1080px] relative overflow-hidden">

        <div className="w-[387px] h-[1080px] absolute left-0 top-0">
          <div className="bg-[#e9e9e9] w-[387px] h-[1080px] absolute left-0 top-0"></div>
        </div>

        <div className="w-[310px] h-[74px] absolute left-[39px] top-[944px]">
          <div className="bg-[#0b163d] rounded-[59px] w-[291px] h-[74px] absolute left-2.5 top-0"></div>

          <div
            className="text-[#fedb41] text-center absolute left-0 top-[26px] w-[310px] h-[23px]"
            style={{ font: "500 20px 'Inter', sans-serif" }}
          >
            Project by Ali Mansab
          </div>
        </div>

        <div className="w-[239px] h-[98px] absolute left-[74px] top-[78px]">
          <img
            className="rounded-[9px] w-[98px] h-[98px] absolute left-0 top-0"
            src="user-image.png"
          />

          <div className="absolute" style={{ inset: "0" }}>
            <div
              className="text-[#000000] text-left absolute left-[123px] top-[23px] w-[116px] h-[17px]"
              style={{ font: "700 20px 'Inter', sans-serif" }}
            >
              Ali Mansab
            </div>

            <div
              className="text-[#000000] text-left absolute left-[123px] top-[57px] w-[116px] h-[17px]"
              style={{ font: "500 13px 'Inter', sans-serif" }}
            >
              18030161040
            </div>
          </div>
        </div>

        <div className="w-[238px] h-[110px] absolute left-[74px] top-[328px]">
          <Link as="/" href="/">
            <div
              className="text-left absolute left-0 top-0 w-[238px] h-[27px]"
              style={{ font: "700 20px 'Inter', sans-serif", color: 'black' }}
            >
              Deployment
            </div>
          </Link>

          <Link as="/models" href="/models">
            <div
              className=" text-left absolute left-0 top-[83px] w-[238px] h-[27px]"
              style={{ font: "500 20px 'Inter', sans-serif", color: 'blue' }}
            >
              Deployed
            </div>
          </Link>


        </div>
        <div className="w-[1250px] h-[110px] absolute right-[200px] top-[328px] bg-[#f3f3f3]">


          <div className="not-prose relative bg-slate-50 rounded-xl overflow-hidden dark:bg-slate-800/25"><div className="absolute inset-0 bg-grid-slate-100 [mask-image:linear-gradient(0deg,#fff,rgba(255,255,255,0.6))] dark:bg-grid-slate-700/25 dark:[mask-image:linear-gradient(0deg,rgba(255,255,255,0.1),rgba(255,255,255,0.5))]"
            style={
              {
                backgroundPosition: "10px 10px"
              }
            }></div><div className="relative rounded-xl overflow-auto">
              <div className="shadow-sm overflow-hidden my-8">
                <table className="border-collapse table-auto w-full text-sm">
                  <thead>
                    <tr>
                      <th className="border-b dark:border-slate-600 font-medium p-4 pl-8 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Model Name</th>
                      <th className="border-b dark:border-slate-600 font-medium p-4 pl-8 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Model Version</th>
                      {/* <th className="border-b dark:border-slate-600 font-medium p-4 pl-8 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Model Handler file</th> */}
                      <th className="border-b dark:border-slate-600 font-medium p-4 pl-8 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Model Archived file</th>
                      {/* <th className="border-b dark:border-slate-600 font-medium p-4 pl-8 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Model Serialized file</th> */}
                      {/* <th className="border-b dark:border-slate-600 font-medium p-4 pl-8 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Model Extra files</th> */}
                      <th className="border-b dark:border-slate-600 font-medium p-4 pr-8 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Model Config file</th>
                      <th className="border-b dark:border-slate-600 font-medium p-4 pl-8 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Model URL</th>
                      <th className="border-b dark:border-slate-600 font-medium p-4 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Model Status</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white dark:bg-slate-800">
                    {
                      data && data.map((model: any, key: any) => (
                        <tr key={key}>
                          <td className="border-b border-slate-100 dark:border-slate-700 p-4 pl-8 text-slate-500 dark:text-slate-400">{model.model_name}</td>
                          <td className="border-b border-slate-100 dark:border-slate-700 p-4 pl-8 text-slate-500 dark:text-slate-400">{model.version}</td>
                          {/* <td className="border-b border-slate-100 dark:border-slate-700 p-4 pl-8 text-slate-500 dark:text-slate-400">{model.handler_file}</td> */}
                          <td className="border-b border-slate-100 dark:border-slate-700 p-4 pl-8 text-slate-500 dark:text-slate-400">{model.archived_model_file}</td>
                          {/* <td className="border-b border-slate-100 dark:border-slate-700 p-4 pl-8 text-slate-500 dark:text-slate-400">{model.serialized_file}</td> */}
                          {/* <td className="border-b border-slate-100 dark:border-slate-700 p-4 pl-8 text-slate-500 dark:text-slate-400">{model.extra_files}</td> */}
                          <td className="border-b border-slate-100 dark:border-slate-700 p-4 pl-8 text-slate-500 dark:text-slate-400">{model.config_file}</td>
                          <a href={model.model_url} target="_blank" rel="noopener noreferrer">
                            <td className="border-b border-slate-100 dark:border-slate-700 p-4 pl-8 text-slate-500 dark:text-slate-400">{model.model_url}</td>
                          </a>
                          <td className="border-b border-slate-100 dark:border-slate-700 p-4 pl-8 text-slate-500 dark:text-slate-400">{model.model_status}</td>
                        </tr>
                      ))
                    }
                  </tbody>
                </table>
              </div>
            </div>
            {/* <div className="absolute inset-0 pointer-events-none border border-black/5 rounded-xl dark:border-white/5">
            </div> */}
          </div>
        </div>
      </div>
    );
  }

};

// Models.getInitialProps = async () => {

//   const res = fetcher("http://127.0.0.1:3520/api/v1/model").then(data => data).catch(err => err)
//   console.log("res", res);

//   return {
//     models: res
//   }
// }
export default Models;