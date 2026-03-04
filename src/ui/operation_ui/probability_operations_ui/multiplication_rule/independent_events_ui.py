        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0">
                <tr>
                    <td valign="middle" style="padding-right: 10px;">
                        <i>P(A &cap; B)</i> = 
                    </td>
                    
                    <td valign="middle">
                        <td align="center";">
                            {self.variable_1_display} &times; {self.variable_2_display}
                        </td>
                    </td>

                    <td valign="middle" style="padding-left: 10px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
            """
        self.dynamic_formula.setText(html_formul)
