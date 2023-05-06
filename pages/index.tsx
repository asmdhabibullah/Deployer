import Link from "next/link";
import { useState, ChangeEvent } from "react";
import fs from "fs";
import { render } from "react-dom";

export interface ModelUploadProps { };

const data = {
  mdl_name: "",
  mdl_file: "",
  ext_file: "",
  hdl_file: "",
  ser_file: ""
};

const ModelUpload = ({ ...props }: ModelUploadProps): JSX.Element => {

  const [modelData, setModelData] = useState(data);

  const formData = new FormData();

  const handInputeleFile = (name: any) => (env: ChangeEvent) => {
    if (env) {
      // console.log(env);
      // setModelData({ ...modelData, [name]: env.target.files[0] });

      let file = env.target.files[0];

      let reader = new FileReader();

      reader.readAsDataURL(file)
      // console.log("file", file.name);



      // formData.append(name, fs.createReadStream(file))
      // formData.append(name, url);

      reader.onload = () => {
        // console.log("reader", reader.result);
        setModelData({ ...modelData, [name]: reader.result })
      };
      reader.onerror = (error) => {
        console.log('Error: ', error);
      }

      // reader.readAsArrayBuffer(file);

    } else {
      // setModelData({ ...modelData, [name]: "" });
    }
  }

  const handInputeleText = (name: any) => (env: ChangeEvent) => {
    if (env) {
      // console.log(env);
      setModelData({ ...modelData, [name]: env.target.value });
      // formData.append(name, env.target.value);

    } else {
      // setModelData({ ...modelData, [name]: "" });
    }
  }

  console.log("modelData", modelData);
  // console.log("formData", formData);

  const handleSubmit = async (env: any) => {
    env.preventDefault();

    // const body = formData.append(modelData);

    // console.log("modelData", modelData);

    const req = await fetch("http://127.0.0.1:3520/api/v1/create-and-start-torch", {
      method: "POST",
      body: JSON.stringify(modelData),
      headers: {
        'Content-Type': 'application/json',
        // 'Content-Type': 'multipart/form-data'
      },
    });

    // console.log("req", );

    await req.json()

    if (req?.status === 200) {
      setModelData(data);
    }
  }

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


      <>

        <label htmlFor="mdl_name" className="w-[564px] h-[313px] absolute left-[529px] top-[32px]" >
          <span>Model Name</span>
          <input type="text" name="mdl_name" id="mdl_name" onChange={handInputeleText("mdl_name")} className="text-[#000]" />
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
            <input hidden type="file" name="mdl_file" id="mdl_file" onChange={handInputeleFile("mdl_file")} />
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
                Upload ext_file file here
              </div>

              <img
                className="w-[105px] h-[105px] absolute left-[137px] top-0"
                src="file-1.png"
              />
            </div>
            <input hidden type="file" name="ext_file" id="ext_file" onChange={handInputeleFile("ext_file")} />
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
                Upload hdl_file file here
              </div>

              <img
                className="w-[105px] h-[105px] absolute left-[137px] top-0"
                src="file-1.png"
              />
            </div>
            <input hidden type="file" name="hdl_file" id="hdl_file" onChange={handInputeleFile("hdl_file")} />
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
                Upload ser_file file here
              </div>

              <img
                className="w-[105px] h-[105px] absolute left-[137px] top-0"
                src="file-1.png"
              />
            </div>
            <input hidden type="file" name="ser_file" id="ser_file" onChange={handInputeleFile("ser_file")} />
          </div>

        </label>

        <div className="w-[437px] h-[98px] absolute left-[935px] top-[969px]">
          <div className="bg-[#0b163d] rounded-[150px] border-solid border-[#ffffff] border w-[437px] h-[98px] absolute left-0 top-0"></div>

          <div
            className="text-[#fedb41] text-center absolute left-16 top-[38px] w-[310px] h-[23px]"
            style={{ font: "700 20px 'Inter', sans-serif" }}
          >
            <button type="submit" onClick={handleSubmit}>
              Start The Deployment
            </button>
          </div>
        </div>
      </>

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