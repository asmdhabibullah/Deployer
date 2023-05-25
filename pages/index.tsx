import { API } from "@/utils";
import Link from "next/link";
import { useState } from "react";

export interface ModelUploadProps { };

// const data = {
//   mdl_name: null,
//   mdl_file: null,
//   ext_file: null,
//   hdl_file: null,
//   ser_file: null
// };

const ModelUpload = ({ ...props }: ModelUploadProps): JSX.Element => {

  const [modelData, setModelData] = useState<{} | any>({});

  const handleInputeleFile = (name: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files && event.target.files[0];
    if (file) {
      // formData.append(name, file);
      setModelData({ ...modelData, [name]: file });
    }
  };

  const handleInputeleText = (name: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value && event.target.value;
    // setModelData(prevFormData => ({ ...prevFormData, [name]: value }));
    setModelData({ ...modelData, [name]: value });
  };

  const handleFolderPath = (name: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      const firstFile = files[0];
      const path = firstFile.webkitRelativePath;
      console.log('Selected Folder Path:', path);
      // Process the selected folder path here
    }
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const finalFormData = new FormData();

    // Append values from formData object to finalFormData
    for (const key in modelData) {
      finalFormData.append(key, modelData[key]);
    }

    console.log("finalFormData", finalFormData);

    fetch(`http://127.0.0.1:3520/api/v1/model/create`, {
      method: "POST",
      body: finalFormData,
    })
      .then(response => response.json())
      .then(data => {
        // Process the successful response
        console.log("data", data);
      })
      .catch(error => {
        // Handle the error response
        console.error("error", error);
      });
  };

  return (
    <div className="bg-[#071135] w-[auto] h-[1200px] relative overflow-hidden">
      <div className="w-[387px] h-[1200px] absolute left-0 top-0">
        <div className="bg-[#e9e9e9] w-[387px] h-[1200px] absolute left-0 top-0"></div>
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
            className="text-[#0038ff] text-left absolute left-0 top-0 w-[238px] h-[27px]"
            style={{ font: "700 20px 'Inter', sans-serif" }}
          >
            Deployment
          </div>
        </Link>

        <Link as="/models" href="/models">
          <div
            className="text-[#1e1e1e] text-left absolute left-0 top-[83px] w-[238px] h-[27px]"
            style={{ font: "500 20px 'Inter', sans-serif" }}
          >
            Deployed
          </div>
        </Link>

      </div>

      <div className="w-[1533px] h-[1200px] absolute left-[387px] top-0">
        <img
          className="w-[1533px] h-[1200px] absolute left-0 top-0"
          src="background-image2.png"
        />
      </div>

      <form onSubmit={handleSubmit}>

        <label htmlFor="mdl_name" className="w-[564px] h-[313px] absolute left-[529px] top-[32px]" >
          <span className="bg-[#000]">Model Name</span>
          <input type="text" name="mdl_name" id="mdl_name" onChange={handleInputeleText("mdl_name")} className="text-[#000]" />
        </label>

        <label htmlFor="version" className="w-[564px] h-[313px] absolute left-[829px] top-[32px]" >
          <span className="bg-[#000]">Version</span>
          <input type="text" name="version" id="version" onChange={handleInputeleText("version")} className="text-[#000]" />
        </label>

        <label htmlFor="mdl_file">
          <div className="w-[564px] h-[313px] absolute left-[529px] top-[132px]">
            <div className="bg-[rgba(13,24,64,0.74)] rounded-[37px] border-dashed border-[#ffffff] border-2 w-[564px] h-[313px] absolute left-0 top-0"></div>

            <div className="w-[378px] h-[149px] absolute left-[93px] top-[82px]">
              <div
                className="text-[#dadada] text-center absolute left-0 top-[125px] w-[378px]"
                style={{ font: "500 20px 'Inter', sans-serif" }}
              >
                Upload model file here
              </div>

              <img
                className="w-[105px] h-[105px] absolute left-[137px] top-0"
                src="file-1.png"
              />

            </div>
            <input hidden type="file" name="mdl_file" id="mdl_file" onChange={handleInputeleFile("mdl_file")} />
          </div>
        </label>

        <label htmlFor="ext_file">

          <div className="w-[564px] h-[313px] absolute left-[1215px] top-[132px]">
            <div className="bg-[rgba(13,24,64,0.74)] rounded-[37px] border-dashed border-[#ffffff] border-2 w-[564px] h-[313px] absolute left-0 top-0"></div>

            <div className="w-[378px] h-[149px] absolute left-[93px] top-[82px]">
              <div
                className="text-[#dadada] text-center absolute left-0 top-[125px] w-[378px]"
                style={{ font: "500 20px 'Inter', sans-serif" }}
              >
                Upload extra file
              </div>

              <img
                className="w-[105px] h-[105px] absolute left-[137px] top-0"
                src="file-1.png"
              />
            </div>
            <input hidden type="file" name="ext_file" id="ext_file" onChange={handleInputeleFile("ext_file")} />
          </div>
        </label>

        <label htmlFor="hdl_file">
          <div className="w-[564px] h-[313px] absolute left-[529px] top-[546px]">
            <div className="bg-[rgba(13,24,64,0.74)] rounded-[37px] border-dashed border-[#ffffff] border-2 w-[564px] h-[313px] absolute left-0 top-0"></div>

            <div className="w-[378px] h-[149px] absolute left-[93px] top-[82px]">
              <div
                className="text-[#dadada] text-center absolute left-0 top-[125px] w-[378px]"
                style={{ font: "500 20px 'Inter', sans-serif" }}
              >
                Upload handler file
              </div>

              <img
                className="w-[105px] h-[105px] absolute left-[137px] top-0"
                src="file-1.png"
              />
            </div>
            <input hidden type="file" name="hdl_file" id="hdl_file" onChange={handleFolderPath("hdl_file")} webkitdirectory="true" />
          </div>

        </label>

        <label htmlFor="ser_file">
          <div className="w-[564px] h-[313px] absolute left-[1215px] top-[546px]">
            <div className="bg-[rgba(13,24,64,0.74)] rounded-[37px] border-dashed border-[#ffffff] border-2 w-[564px] h-[313px] absolute left-0 top-0"></div>

            <div className="w-[378px] h-[149px] absolute left-[93px] top-[82px]">
              <div
                className="text-[#dadada] text-center absolute left-0 top-[125px] w-[378px]"
                style={{ font: "500 20px 'Inter', sans-serif" }}
              >
                Upload serialized file
              </div>

              <img
                className="w-[105px] h-[105px] absolute left-[137px] top-0"
                src="file-1.png"
              />
            </div>
            <input hidden type="file" name="ser_file" id="ser_file" onChange={handleInputeleFile("ser_file")} />
          </div>

        </label>

        <div className="w-[437px] h-[98px] absolute left-[935px] top-[969px]">
          <div className="bg-[#0b163d] rounded-[150px] border-solid border-[#ffffff] border w-[437px] h-[98px] absolute left-0 top-0"></div>

          <div
            className="text-[#fedb41] text-center absolute left-16 top-[38px] w-[310px] h-[23px]"
            style={{ font: "700 20px 'Inter', sans-serif" }}
          >
            <button type="submit">
              Start Deployment
            </button>
          </div>
        </div>
      </form>

      <div className="w-[310px] h-[74px] absolute left-[39px] top-[1067px]">
        <div className="bg-[#0b163d] rounded-[59px] w-[291px] h-[74px] absolute left-2.5 top-0"></div>

        <div
          className="text-[#fedb41] text-center absolute left-0 top-[26px] w-[310px] h-[23px]"
          style={{ font: "500 20px 'Inter', sans-serif" }}
        >
          Project by Ali Mansab
        </div>
      </div>
    </div>
  );
};

export default ModelUpload;



  // console.log(API);

  // const handleInputeleFile = (name: any) => (env: any) => {
  //   if (env) {
  //     // console.log(env);
  //     // setModelData({ ...modelData, [name]: env.target.files[0] });

  //     let file = env?.target?.files[0];

  //     formData.append(name, file);

  //     // let reader = new FileReader();

  //     // reader.readAsDataURL(file)
  //     // console.log("file", file.name);

  //     // formData.append(name, fs.createReadStream(file))
  //     // formData.append(name, url);

  //     // reader.onload = (e) => {
  //     //   const path = e.target?.result;
  //     //   // console.log("reader", reader.result);
  //     //   setModelData({ ...modelData, [name]: path })
  //     //   // setModelData({ ...modelData, [name]: reader.result })
  //     // }
  //     // reader.readAsDataURL(file);
  //     // // reader.onerror = (error) => {
  //     //   console.log('Error: ', error);
  //     // }
  //     // reader.readAsArrayBuffer(file);
  //   } else {
  //     // setModelData({ ...modelData, [name]: "" });
  //     console.log("Something wrong!");
  //   }
  // }

  // const handleInputeleText = (name: any) => (env: any) => {
  //   if (env) {
  //     // console.log(env);
  //     // setModelData({ ...modelData, [name]: env.target.value });
  //     formData.append(name, env.target.value);

  //   } else {
  //     // setModelData({ ...modelData, [name]: "" });
  //   }
  // }

  // // console.log("modelData", modelData);

  // const handleSubmit = async (env: any) => {
  //   env.preventDefault();

  //   console.log("formData", formData);

  //   fetch("http://127.0.0.1:3520/api/v1/model/create", {
  //     method: "POST",
  //     body: formData,
  //     // body: JSON.stringify(modelData),
  //     // headers: {
  //     //   'Content-Type': 'application/json',
  //     //   // 'Content-Type': 'multipart/form-data'
  //     // },
  //   })
  //     .then(response => response.json())
  //     .then(data => {
  //       // Process the successful response
  //       console.log(data);
  //     })
  //     .catch(error => {
  //       // Handle the error response
  //       console.error("error", error);
  //     });
  // }
