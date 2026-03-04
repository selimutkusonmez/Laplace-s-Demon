        html_formul = f"""
                    <table align="center" cellpadding="0" cellspacing="0" >
                        <tr>
                            <td valign="middle" style="padding-right: 15px;">
                                <i>P(X = {self.variable_2_display})</i> = 
                            </td>
                            
                            <td valign="middle">
                                {self.variable_1_display}<sup>{self.variable_2_display}</sup>(1 - {self.variable_1_display})<sup>1 - {self.variable_2_display}</sup>
                            </td>

                            <td valign="middle" style="padding-left: 20px;">
                                = {self.current_result}
                            </td>
                        </tr>
                    </table>
                """
        self.dynamic_formula.setText(html_formul)


        