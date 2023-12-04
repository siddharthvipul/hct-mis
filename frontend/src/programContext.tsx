import React, {
  createContext,
  ReactElement,
  useContext,
  useState,
} from 'react';
import { ProgramStatus } from './__generated__/graphql';

export interface ProgramInterface {
  id: string;
  name: string;
  status: ProgramStatus;
  individualDataNeeded: boolean;
  dataCollectingType: {
    id: string;
    householdFiltersAvailable: boolean;
    individualFiltersAvailable: boolean;
  };
}

export type ProgramContextType = ProgramInterface | null;

export const ProgramContext = createContext(null);

export const ProgramProvider = ({ children }): ReactElement => {
  const [selectedProgram, setSelectedProgram] = useState<ProgramContextType>(
    null,
  );
  const isActiveProgram = selectedProgram?.status === ProgramStatus.Active;

  return (
    <ProgramContext.Provider
      value={{ selectedProgram, setSelectedProgram, isActiveProgram }}
    >
      {children}
    </ProgramContext.Provider>
  );
};

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
export const useProgramContext = () => useContext(ProgramContext);
