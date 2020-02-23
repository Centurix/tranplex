<template>
  <v-app id="inspire">
    <transplex-navigation></transplex-navigation>
    <transplex-header></transplex-header>
    <router-view></router-view>
    <transplex-footer></transplex-footer>
  </v-app>
</template>

<script>
import TransplexHeader from '@/components/TransplexHeader.vue'
import TransplexNavigation from "@/components/TransplexNavigation"
import TransplexFooter from "@/components/TransplexFooter"

export default {
  components: {
    TransplexHeader,
    TransplexNavigation,
    TransplexFooter
  },
  props: {
    source: String,
  },
  methods: {
  },
  data: () => ({
  }),
  created () {
    this.$vuetify.theme.dark = true
  },
}
</script>
