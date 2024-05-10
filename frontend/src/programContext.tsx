import { createContext, ReactElement, useContext, useState } from 'react';
import { DataCollectingTypeType, ProgramStatus } from './__generated__/graphql';

export interface ProgramInterface {
  id: string;
  name: string;
  status: ProgramStatus;
  dataCollectingType: {
    id: string;
    householdFiltersAvailable: boolean;
    individualFiltersAvailable: boolean;
    label: string;
    code: string;
    type: string;
    children;
  };
}

export type ProgramContextType = ProgramInterface | null;

export const ProgramContext = createContext(null);

export function ProgramProvider({
  children,
}: {
  children: React.ReactNode;
}): ReactElement {
  const [selectedProgram, setSelectedProgram] =
    useState<ProgramContextType>(null);
  let isActiveProgram = selectedProgram?.status === ProgramStatus.Active;
  const isSocialDctType =
    selectedProgram?.dataCollectingType?.type?.toUpperCase() ===
    DataCollectingTypeType.Social;
  const isStandardDctType =
    selectedProgram?.dataCollectingType?.type?.toUpperCase() ===
    DataCollectingTypeType.Standard;

  // Set isActiveProgram to true if All Programs is selected
  if (selectedProgram === null) {
    isActiveProgram = true;
  }
  return (
    <ProgramContext.Provider
      value={{
        selectedProgram,
        setSelectedProgram,
        isActiveProgram,
        isSocialDctType,
        isStandardDctType,
      }}
    >
      {children}
    </ProgramContext.Provider>
  );
}

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
export const useProgramContext = () => useContext(ProgramContext);
