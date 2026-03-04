        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0">
                <tr>
                    <td valign="middle">
                        <i>F({self.variable_3_display})</i> = 1 &minus; 
                    </td>
                    
                    <td valign="middle" style="font-size: 50px; font-weight: 300; padding-bottom: 5px;">
                        (
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor;">
                                    <i>{self.variable_2_display}</i>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" >
                                    <i>{self.variable_3_display}</i>
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="font-size: 50px; font-weight: 300; padding-bottom: 5px;">
                        )
                    </td>
                    
                    <td valign="top" >
                        {self.variable_1_display}
                    </td>

                    <td valign="middle" >
                        , <i>{self.variable_3_display}</i> &ge; <i>{self.variable_2_display}</i>
                    </td>

                    <td valign="middle" >
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)


        