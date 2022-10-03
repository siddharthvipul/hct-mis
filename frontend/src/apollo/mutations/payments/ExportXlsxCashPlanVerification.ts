import { gql } from 'apollo-boost';

export const ExportXlsxPaymentVerificationPlanFile = gql`
  mutation ExportXlsxPaymentVerificationPlanFile($paymentVerificationPlanId: ID!) {
    exportXlsxPaymentVerificationPlanFile(paymentVerificationPlanId: $paymentVerificationPlanId) {
      cashPlan {
        id
        # verificationPlans {
        #   edges {
        #     node {
        #       id
        #       xlsxFileExporting
        #       hasXlsxFile
        #       xlsxFileWasDownloaded
        #       xlsxFileImported
        #     }
        #   }
        # }
      }
    }
  }
`;
