
html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle">
                        <i>P(X = {self.variable_3_display})</i> = 
                    </td>
                    
                    <td valign="middle" style="font-size: 50px; font-weight: 200;">
                        (
                    </td>
                    
                    <td valign="middle" align="center">
                        <table cellpadding="0" cellspacing="0" style="font-size: 30px;">
                            <tr><td align="center">{self.variable_1_display}</td></tr>
                            <tr><td align="center">{self.variable_3_display}</td></tr>
                        </table>
                    </td>
                    
                    <td valign="middle" style="font-size: 50px; font-weight: 200;">
                        )
                    </td>

                    <td valign="middle">
                        {self.variable_2_display}<sup>{self.variable_3_display}</sup>(1 - {self.variable_2_display})<sup>{self.variable_1_display} - {self.variable_3_display}</sup>
                    </td>

                    <td valign="middle">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)