import pandas as pd
import numpy as np
from io import BytesIO

class SingleCaseData:
    def __init__(self, values=None, phase=None, case=None, B_start=None, mt=None, 
                 phase_design=None, phase_starts=None, name=None, dvar="values", 
                 pvar="phase", mvar="mt", data=None, **kwargs):
        
        # If data is provided as a DataFrame, extract values, phase, and case directly
        if data is not None:
            self.df = data.copy()
            self.values = self.df[dvar].values if dvar in self.df.columns else None
            self.phase = self.df[pvar].values if pvar in self.df.columns else None
            self.case = self.df['case'].values if 'case' in self.df.columns else None
            self.mt = self.df[mvar].values if mvar in self.df.columns else list(range(1, len(self.values) + 1))
        else:
            self.values = values
            self.phase = phase
            self.case = case if isinstance(case, list) else [case] * len(values) if case else None
            self.mt = mt if mt is not None else list(range(1, len(values) + 1))

        # Set default variable labels
        self.dvar = dvar
        self.pvar = pvar
        self.mvar = mvar
        self.name = name
        self.phase_design = phase_design if phase_design is not None else {}
        self.phase_starts = phase_starts

        # If phase_design or phase_starts is provided, use it; otherwise, set from phase or B_start
        if phase_design:
            self._apply_phase_design()
        elif phase_starts:
            self._set_phase_design_from_phase_starts()
        elif B_start:
            self._set_phase_design_from_B_start(B_start)
        elif phase:
            self._set_phase_design_from_phase(phase)

        # Construct DataFrame
        self.df = pd.DataFrame({
            self.dvar: self.values,
            self.mvar: self.mt
        })
        
        # Apply phase design to DataFrame if present
        if self.phase_design:
            self.df[self.pvar] = np.repeat(list(self.phase_design.keys()), list(self.phase_design.values()))
        else:
            # Default to phase "A" if no design is specified
            self.df[self.pvar] = self.phase if self.phase is not None else ['A'] * len(self.values)
        
        if self.case is not None:
            self.df['case'] = self.case

    def _apply_phase_design(self):
        total_count = sum(self.phase_design.values())
        if total_count < len(self.values):
            extra_phase = len(self.values) - total_count
            self.phase_design[list(self.phase_design.keys())[-1]] += extra_phase

    def _set_phase_design_from_phase(self, phase):
        phase_counts = pd.Series(phase).value_counts().sort_index()
        self.phase_design = {name: count for name, count in zip(phase_counts.index, phase_counts.values)}

    def _set_phase_design_from_B_start(self, B_start):
        A_length = B_start - 1
        B_length = len(self.values) - A_length
        self.phase_design = {"A": A_length, "B": B_length}

    def _set_phase_design_from_phase_starts(self):
        start_points = sorted(self.phase_starts.items(), key=lambda x: x[1])
        self.phase_design = {}
        for i in range(len(start_points) - 1):
            self.phase_design[start_points[i][0]] = start_points[i + 1][1] - start_points[i][1]
        last_phase = start_points[-1][0]
        last_phase_length = len(self.values) - start_points[-1][1] + 1
        self.phase_design[last_phase] = last_phase_length

    def export(self, filename=None, format="html", caption=None, footnote=None, round_decimals=2, columns=None):
        export_df = self.df.copy()
        
        if round_decimals is not None:
            export_df = export_df.round(round_decimals)
        
        if columns:
            export_df = export_df[columns]
        
        if format == "html":
            html_content = export_df.to_html(index=False)
            if caption:
                html_content = f"<h3>{caption}</h3>\n" + html_content
            if footnote:
                html_content += f"\n<p><em>{footnote}</em></p>"
            
            if filename:
                with open(filename, "w") as file:
                    file.write(html_content)
            else:
                return html_content
        
        elif format == "csv":
            if filename:
                export_df.to_csv(filename, index=False)
            else:
                return export_df.to_csv(index=False)
        
        elif format == "xlsx":
            if filename:
                export_df.to_excel(filename, index=False)
            else:
                buffer = BytesIO()
                export_df.to_excel(buffer, index=False)
                buffer.seek(0)
                return buffer
        
        else:
            raise ValueError("Format not supported. Please use 'html', 'csv', or 'xlsx'.")

    @staticmethod
    def as_long_dataframe(cases, l2=None, id='case'):
        data_frames = []
        for case in cases:
            df = case.df.copy()
            df[id] = case.name  # Add case name as an identifier
            data_frames.append(df)

        long_df = pd.concat(data_frames, ignore_index=True)

        if l2 is not None:
            long_df = long_df.merge(l2, left_on=id, right_on=id, how='left')

        return long_df

    def __str__(self):
        name_str = f"Case Name: {self.name}" if self.name else "Unnamed Case"
        return f"{name_str}\nData:\n{self.df}\n"
