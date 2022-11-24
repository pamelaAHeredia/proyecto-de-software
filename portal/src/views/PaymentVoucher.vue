<template>
  <div class="container">
    <form v-on:submit.prevent="submitForm">
      <input
        accept=".png, .jpg, .jpeg, .pdf"
        type="file"
        id="fileInput"
        ref="fileInput"
        placeholder="edit me"
        v-on:change="onChangeFileUpload(this)"
      />
      <input type="number" placeholder="Monto" />
      <input type="text" placeholder="Descripcion" />
      <button v-on:click="submitForm()">Upload</button>
    </form>
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
      const id = JSON.parse(sessionStorage.getItem("currentUser")).Id;
      console.log(`El ID es: ${id}`);
      formData.append("image", this.file);
      const headers = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      axios
        .post(`${PATH_SERVER}/api/me/payment/${id}`, formData, headers)
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
