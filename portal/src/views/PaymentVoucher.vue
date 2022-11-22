<template>
  <div class="container">
    <input
      accept=".png, .jpg, .jpeg,"
      type="file"
      id="fileInput"
      ref="fileInput"
      placeholder="edit me"
      v-on:change="onChangeFileUpload(this)"
    />
    <input type="number" placeholder="Monto" />
    <input type="text" placeholder="Descripcion" />
    <button v-on:click="submitForm()">Upload</button>
  </div>
</template>

<script>
import axios from "axios";
const PATH_SERVER = import.meta.env.VITE_APP_PATH_API;
axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";

export default {
  data() {
    return {
      file: null,
    };
  },
  methods: {
    submitForm() {
      const formData = new FormData();
      formData.append("image", this.file);
      //formData.append("image", this.file);
      //formData.append("image", this.file);
      //formData.append("image", this.file);
      axios
        .post(`${PATH_SERVER}/api/me/payment/1`, {
          formData,
        })
        .then((response) => {
          console.log(response);
        })
        .catch((e) => console.log(e));
    },
    onChangeFileUpload() {
      this.file = document.querySelector("#fileInput").files[0];
      console.log(this.file);
      /*const fileReader = new FileReader();
      fileReader.addEventListener("load", () => {
        this.imageUrl = fileReader.result;
      });
      fileReader.readAsDataURL(this.file[0]);
      this.image = files[0];*/
    },
  },
};
</script>

<style></style>
