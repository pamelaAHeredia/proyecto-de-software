<template>
  <div class="container">
    <h1 class="text-center">Cargar pago de {{ useSelect.get_current.name }}</h1>
    <form v-on:submit.prevent="submitForm">
      <div class="mb-3">
        <label class="form-label">Seleccione un comprobante de pago</label>
        <input
          class="form-control form-control-lg"
          accept=".png, .jpg, .jpeg, .pdf"
          type="file"
          id="fileInput"
          ref="fileInput"
          placeholder="Selecciona un archivo"
          v-on:change="onChangeFileUpload(this)"
        />
      </div>
      <div class="mb-3">
        <label class="form-label">Ingrese un monto</label>
        <input
          class="form-control form-control-lg"
          v-model="amount"
          type="number"
          placeholder="Monto"
        />
      </div>
      <div class="mb-3">
        <label class="form-label">Ingrese una descripcion</label>
        <input
          class="form-control form-control-lg"
          v-model="description"
          type="text"
          placeholder="Descripcion"
        />
      </div>
      <div class="mb-3">
        <button type="submit" class="btn btn-primary">Cargar pago</button>
      </div>
    </form>
  </div>
</template>

<script>
import { useSelectMember } from "../stores/useSelect";
import { apiService } from "@/api";
export default {
  setup() {
    const useSelect = useSelectMember();
    return { useSelect };
  },
  data() {
    return {
      file: null,
      amount: null,
      description: "",
    };
  },
  methods: {
    async submitForm() {
      const formData = new FormData();
      formData.append("image", this.file);
      formData.append("amount", this.amount);
      formData.append("description", this.description);
      const access_token = sessionStorage.getItem("token");
      const headers = {
        headers: {
          Authorization: access_token,
          "Content-Type": "multipart/form-data",
        },
      };
      await apiService
        .post(
          `/api/me/payment/${this.useSelect.get_current.id}`,
          formData,
          headers
        )
        .then((response) => {
          console.log(response);
          alert("Se cargo el pago correctamente");
        })
        .catch((e) => console.log(e));
    },
    onChangeFileUpload() {
      this.file = document.querySelector("#fileInput").files[0];
      console.log(this.amount);
      console.log(this.description);
    },
  },
};
</script>

<style scope>
.container h1 {
  margin-bottom: 15px;
  font-size: 60px;
  color: #333333;
}
.filter {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  background: #333333;
}

.custom-shape-divider-bottom-1669129895 {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  overflow: hidden;
  line-height: 0;
  transform: rotate(180deg);
}

.custom-shape-divider-bottom-1669129895 svg {
  position: relative;
  display: block;
  width: calc(231% + 1.3px);
  height: 500px;
  transform: rotateY(180deg);
}

.custom-shape-divider-bottom-1669129895 .shape-fill {
  fill: #333333;
}
</style>
